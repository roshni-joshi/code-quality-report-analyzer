package code.quality.analyzer.util;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.transport.URIish;

import java.io.File;

/**
 * A class for interacting with Git repositories.
 * Currently, it provides method for cloning repositories from a remote URL to a local directory.
 * It uses jgit dependency.
 */
public class GitRepository {
    private String remoteRepoURL; // URL of remote git repository.
    private String localRepoBasePath; // Base path for local repository.
    private String localRepoFullPath; // Full path of the local repository. (This is formed using remote URL & base path.)

    /**
     * Constructs a GitRepository class object, with the specified remote repository URL and local base path.
     * Also, assigns a value for localRepoFullPath using remoteRepoURL and local base path.
     * Eg: If remoteRepoURL="https://github.com/foo/bar.git" and localBasePath="MyFolder"
     * Then, localRepoFullPath becomes "MyFolder/bar"
     *
     * @param remoteURL     The URL of the remote Git repository.
     * @param localBasePath The base path where the local repository will be stored.
     */
    public GitRepository(String remoteURL, String localBasePath) {
        this.remoteRepoURL = remoteURL;
        this.localRepoBasePath = localBasePath;
        try {
            localRepoFullPath = localRepoBasePath + "/" + new URIish(remoteURL).getHumanishName();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Clones the remote Git repository to the local directory.
     * If the local repository already exists, cloning is skipped.
     */
    public void cloneRepo() {

        File localRepo = new File(localRepoFullPath);

        // Check if the local repository already exists or not.
        if (localRepo.exists()) {
            System.out.println("Cloning Skipped. Already found cloned repository: " + localRepoFullPath);
        }
        // Clone, if it doesn't exist yet.
        else {
            try {
                Git.cloneRepository().setURI(remoteRepoURL).setDirectory(new File(localRepoFullPath)).call().close();
                System.out.println("Repository " + remoteRepoURL + " cloned successfully at " + localRepoFullPath);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * Returns the Full Local Path of current git repository.
     * @return String Local Repo full-path(absolute).
     * @throws Exception
     */
    public String getLocalRepoFullPath() {
        return new File(localRepoFullPath).getAbsolutePath();
    }
}
