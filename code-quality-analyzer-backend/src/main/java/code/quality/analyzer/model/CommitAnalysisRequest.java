package code.quality.analyzer.model;

public class CommitAnalysisRequest {

	private String gitRepoLink;
	private String branch;
	private String commitId;
	private int noOfCommits;
	
	public String getGitRepoLink() {
		return gitRepoLink;
	}
	public void setGitRepoLink(String gitRepoLink) {
		this.gitRepoLink = gitRepoLink;
	}
	public String getBranch() {
		return branch;
	}
	public void setBranch(String branch) {
		this.branch = branch;
	}
	public String getCommitId() {
		return commitId;
	}
	public void setCommitId(String commitId) {
		this.commitId = commitId;
	}
	public int getNoOfCommits() {
		return noOfCommits;
	}
	public void setNoOfCommits(int noOfCommits) {
		this.noOfCommits = noOfCommits;
	}
}
