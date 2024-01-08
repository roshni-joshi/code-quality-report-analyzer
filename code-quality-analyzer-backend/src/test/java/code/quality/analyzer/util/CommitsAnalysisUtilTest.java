/**
 *
 */
package code.quality.analyzer.util;

import static code.quality.analyzer.util.Constants.*;
import static org.junit.jupiter.api.Assertions.*;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

import org.eclipse.jgit.api.errors.InvalidRefNameException;
import org.eclipse.jgit.api.errors.RefNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;

import code.quality.analyzer.exception.InvalidCommitsException;

/**
 * Test CommitsAnalysisUtil class methods
 */
class CommitsAnalysisUtilTest {

	private static List<String> commitIds = null;
	private static String repoPath;

	@BeforeEach
	void setUp() {
		commitIds = new ArrayList<String>();
		repoPath = CommitsAnalysisUtil.cloneRepository(REPO_URL);
	}

	@Test
	void testGetCommitIdsForOneCommitAndHotspot() throws Exception {
		commitIds.add(COMMIT1);
		List<String> ids = new ArrayList<String>(CommitsAnalysisUtil.getCommitIds(repoPath, BRANCH, ONE).keySet());
		assertEquals(commitIds, ids);
	}
	
	@ParameterizedTest
	@CsvSource({"2,2", "1,1", "5,5", "0,0"})
	void testGetCommitIdsForTrend(int noOfCommits, int expectedSize) throws Exception {
		Map<String, String> commitsData = CommitsAnalysisUtil.getCommitIds(repoPath, BRANCH, noOfCommits);
		assertEquals(expectedSize, commitsData.size());
	}

	@Test
	void testGetCommitIdsForTrendShouldHaveUsers() throws Exception {

		Map<String, String> expectedCommitsData = new HashMap<>();
		expectedCommitsData.put(COMMIT1, USER1);
		expectedCommitsData.put(COMMIT2, USER2);

		Map<String, String> commitsData = CommitsAnalysisUtil.getCommitIds(repoPath, BRANCH, TOTAL_COMMITS_2);
		assertEquals(expectedCommitsData, commitsData);

	}

	@Test
	void testGetCommitIdsExceptionRefNotFound() throws Exception {
		assertThrows(RefNotFoundException.class, () -> CommitsAnalysisUtil.getCommitIds(repoPath, "abc", Constants.ONE));
	}

	@Test
	void testGetCommitIdsExceptionInvalidRefNameWithSpace() throws Exception {
		assertThrows(InvalidRefNameException.class, () -> CommitsAnalysisUtil.getCommitIds(repoPath, " ", Constants.ONE));
	}

	@Test
	void testGetCommitIdsExceptionInvalidRefNameWithNull() throws Exception {
		assertThrows(InvalidRefNameException.class, () -> CommitsAnalysisUtil.getCommitIds(repoPath, null, Constants.ONE));
	}

	@ParameterizedTest
	@MethodSource("invalidRepo")
	void testGetCommitIdsExceptionInvalidRepo(String repo) throws Exception {
		assertThrows(RefNotFoundException.class, () -> CommitsAnalysisUtil.getCommitIds(repo, BRANCH, ONE));
	}
	
	@Test
	void testGenerateReportsForOneCommitAndHotspot() throws Exception {
		commitIds.add(COMMIT1);
		String path = CommitsAnalysisUtil.generateReports(commitIds, repoPath, BRANCH);
		assertTrue(Files.exists(Paths.get(path)));
	}
	
	@Test
	void testGenerateReportsForExceptionWithNullList() {
		assertThrows(InvalidCommitsException.class, () -> CommitsAnalysisUtil.generateReports(null, repoPath, BRANCH));
	}

	@Test
	void testGenerateReportsForExceptionWithEmptyList() {
		List<String> emptyList = new ArrayList<>();
		assertThrows(InvalidCommitsException.class, () -> CommitsAnalysisUtil.generateReports(emptyList, repoPath, BRANCH));
	}

	@Test
	void testGenerateReportsForTrend() throws Exception {
		commitIds.add(COMMIT1);
		commitIds.add(COMMIT2);
		commitIds.add(COMMIT3);

		String path = CommitsAnalysisUtil.generateReports(commitIds, repoPath, BRANCH);

		assertTrue(checkCommitFolders(path,commitIds));
	}
	
	private static Stream<String> invalidRepo() {
        return Stream.of(EMPTY, null);
    }

	/**
	 * Checks the validity of commit folders.
	 * @param path base report path
	 * @param commitIds List of string commit ids
	 * @return true if all commits folders are valid, else false.
	 */
	private static boolean checkCommitFolders(String path, List<String> commitIds) {

		for (String commitId: commitIds) {

			if (!Files.exists(Paths.get(path).resolve(commitId)))
			{
				return false;
			}
		}
		return true;
	}
}
