package code.quality.analyzer.service.report.generate;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;

import code.quality.analyzer.exception.InvalidCommitsException;
import code.quality.analyzer.model.CommitAnalysisRequest;
import code.quality.analyzer.model.HotspotAnalysisRequest;
import code.quality.analyzer.model.OneCommitAnalysisRequest;
import code.quality.analyzer.model.TrendAnalysisRequest;
import code.quality.analyzer.util.CommitsAnalysisUtil;
import code.quality.analyzer.util.Constants;

@Service
public class GenerateReportServiceImpl implements GenerateReportService {

	private static Logger logger = LogManager.getLogger(GenerateReportServiceImpl.class);
	
	private String repoPath, branch, commitId;
	private int noOfCommits;
	
	@Override
	public OneCommitAnalysisRequest generateOneCommitReport(CommitAnalysisRequest commitAnalysisRequest) throws Exception {
		logger.info("BEGIN generateOneCommitReport()");
		List<String> commitIds = null;
		setData(commitAnalysisRequest);
		CommitsAnalysisUtil.checkoutAndValidate(repoPath, branch);
		//If commit id is null or empty, last commit id will be fetched for analysis
		if(commitId == null || commitId.isBlank()) {
			commitIds = new ArrayList<String>(CommitsAnalysisUtil.getCommitIds(repoPath, branch, Constants.ONE).keySet());
		} else {
			commitIds = new ArrayList<String>();
			commitIds.add(commitId);
		}
		String reportPath = CommitsAnalysisUtil.generateReports(commitIds, repoPath, branch);
		OneCommitAnalysisRequest request = new OneCommitAnalysisRequest();
		request.setReportPath(reportPath);
		return request;
	}

	@Override
	public TrendAnalysisRequest generateTrendAnalysisReport(CommitAnalysisRequest commitAnalysisRequest) throws Exception {
		logger.info("BEGIN generateTrendAnalysisReport()");
		setData(commitAnalysisRequest);
		if(noOfCommits == 0) {
			throw new InvalidCommitsException("Invalid number of commits");
		}
		Map<String, String> commitsData = CommitsAnalysisUtil.getCommitIds(repoPath, branch, noOfCommits+1);
		List<String> commitIds = new ArrayList<String>(commitsData.keySet());
		String reportPath = CommitsAnalysisUtil.generateReports(commitIds, repoPath, branch);
		Map<String, String> previousCommit = null;
		if(commitIds.size() == noOfCommits+1) {
			previousCommit = new HashMap<String, String>();
			String previousCommitId = commitIds.get(commitIds.size()-1);
			String previousUser = commitsData.remove(previousCommitId);
			previousCommit.put(previousCommitId, previousUser);
		}
		TrendAnalysisRequest request = new TrendAnalysisRequest();
		request.setCommitsData(commitsData);
		request.setPreviousCommit(previousCommit);
		request.setReportPath(reportPath);
		return request;
	}

	@Override
	public HotspotAnalysisRequest generateHotspotReport(CommitAnalysisRequest commitAnalysisRequest) throws Exception {
		logger.info("BEGIN generateHotspotReport()");
		setData(commitAnalysisRequest);
		CommitsAnalysisUtil.checkoutAndValidate(repoPath, branch);
		List<String> commitIds = new ArrayList<String>(CommitsAnalysisUtil.getCommitIds(repoPath, branch, Constants.ONE).keySet());
		String reportPath = CommitsAnalysisUtil.generateReports(commitIds, repoPath, branch);
		HotspotAnalysisRequest request = new HotspotAnalysisRequest();
		request.setReportPath(reportPath);
		return request;
	}

	private void setData(CommitAnalysisRequest commitAnalysisRequest) {
		logger.info("BEGIN setData()");
		repoPath = CommitsAnalysisUtil.cloneRepository(commitAnalysisRequest.getGitRepoLink());
		branch = commitAnalysisRequest.getBranch();
		commitId = commitAnalysisRequest.getCommitId();
		noOfCommits = commitAnalysisRequest.getNoOfCommits();
	}
}
