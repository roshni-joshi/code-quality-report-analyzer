import axios from "axios";

const api = () => {
  const API_URL = `https://api.github.com`;

  const fetchBranches = async (repoLink) => {
    if (!repoLink) {
      console.error("Repo link is undefined");
      return [];
    }
    const ownerAndRepo = repoLink.replace(/\.git$/, '').split('/').slice(-2).join('/');
    const branchUrl = `${API_URL}/repos/${ownerAndRepo}/branches`;

    try {
      const response = await axios.get(branchUrl);
      const branchOptions = response.data.map((branch) => ({
        value: branch.name,
        label: branch.name,
      }));
      return branchOptions;
    } catch (error) {
      console.error("Error fetching branches:", error);
      throw error;
    }
  };

  const fetchCommits = async (repoLink, branch) => {
    console.log(branch);
    if (!repoLink || !branch){
      // Handle the case where repoLink is undefined
      console.error("Repo link is undefined");
      return [];
    }

    const ownerAndRepo = repoLink.replace(/\.git$/, '').split('/').slice(-2).join('/');
    const commitsUrl = `${API_URL}/repos/${ownerAndRepo}/commits?sha=${branch.value}`;
    try {
      const response = await axios.get(commitsUrl);
      const commitOptions = response.data.slice(0, 10).map((commit) => ({
        value: commit.sha,
        label: `#${commit.sha.substring(0, 7)} - ${commit.commit.message}`,
      }));
      console.log(commitOptions);
      return commitOptions;
    } catch (error) {
      console.error("Error fetching commits:", error);
      throw error;
    }
  };

  return { fetchBranches, fetchCommits };
};

export default api;

