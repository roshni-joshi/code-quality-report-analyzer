package code.quality.analyzer.util;

import java.util.*;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.eclipse.jgit.api.CreateBranchCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.internal.storage.file.FileRepository;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;

import Designite.Designite;
import code.quality.analyzer.exception.InvalidCommitsException;

public class CommitsAnalysisUtil {
	
	private static Logger logger = LogManager.getLogger(CommitsAnalysisUtil.class);

	/**
	 * Clone git repository
	 * @param gitRepoLink git repository link
	 * @return cloned repository path
	 */
	public static String cloneRepository(String gitRepoLink) {
		logger.info("BEGIN cloneRepository()");
		GitRepository gitRepository = new GitRepository(gitRepoLink, Constants.REPO_PATH);
		gitRepository.cloneRepo();
		return gitRepository.getLocalRepoFullPath();
	}
	
	/**
	 * Fetch commit ids and user info for given repository and number of commits
	 * @param repoPath repository path
	 * @param branchname branch name
	 * @param noOfCommits number of commits
	 * @return Map<String, String> commits id and username
	 * @throws Exception
	 */
	public static Map<String, String> getCommitIds(String repoPath, String branchname, int noOfCommits) throws Exception {
		logger.info("BEGIN getCommitIds()");
		Map<String, String> commitsData = new LinkedHashMap<String, String>();
		if (noOfCommits == 0) {
			return commitsData;
		}
		Git git = checkoutAndValidate(repoPath, branchname);
		Iterable<RevCommit> commits = git.log().setMaxCount(noOfCommits).call();
		commits.forEach(commit -> commitsData.put(commit.getName(), commit.getAuthorIdent().getName()));
		return commitsData;
	}
	
	/**
	 * Validate repoPath and branch name. Checkout to given branch
	 * @param repoPath repository path
	 * @param branchname branch name
	 * @return Git git repository with checked out branch
	 * @throws Exception
	 */
	public static Git checkoutAndValidate(String repoPath, String branchname) throws Exception {
		logger.info("BEGIN checkoutAndValidate()");
		Repository repository = new FileRepository(repoPath + Constants.REPO_SUFFIX);
		Git git = new Git(repository);
		boolean branchNotNullNotEmpty = branchname!= null && !branchname.isBlank();
		if(branchNotNullNotEmpty && repository.findRef(Constants.BRANCH_PREFIX + branchname) == null) {
			git.checkout().setCreateBranch(true).setName(branchname)
			.setUpstreamMode(CreateBranchCommand.SetupUpstreamMode.SET_UPSTREAM)
			.setStartPoint(Constants.REMOTE_ORIGIN + branchname).call();
		} else {
			git.checkout().setCreateBranch(false).setName(branchname).call();
		}
		return git;
	}
	
	/**
	 * generate report for given number of commits using designite
	 * @param commitIds from and to commit ids
	 * @param repoPath repository path
	 * @param branch branch name
	 * @return String commits report path
	 * @throws Exception
	 */
	public static String generateReports(List<String> commitIds, String repoPath, String branch) throws Exception {
		logger.info("BEGIN generateReports()");
		if(commitIds == null || commitIds.isEmpty()) {
			throw new InvalidCommitsException("Invalid commits");
		}
		String reportPath = repoPath + Constants.REPORT_PATH;
		String fromCommit = commitIds.get(0);
		if(!commitIds.isEmpty() && commitIds.size() != 1) {
			fromCommit = commitIds.get(commitIds.size()-1);
		}

		List<String> arguments = new ArrayList<>();
		arguments.addAll(Arrays.asList("-i", repoPath));
		arguments.addAll(Arrays.asList("-o", reportPath));
		arguments.addAll(Arrays.asList("-ac", Constants.BRANCH_PREFIX + branch));
		arguments.addAll(Arrays.asList("-fr", fromCommit));
		arguments.addAll(Arrays.asList("-to", commitIds.get(0)));

		String[] args = arguments.toArray(String[]::new);

		Designite.main(args);
		if(commitIds.size() == 1) {
			reportPath = reportPath + "/" + commitIds.get(0);
		}
		return reportPath;
	}
}
