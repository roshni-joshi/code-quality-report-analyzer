package code.quality.analyzer.util;

public class Constants {
	public static String EMPTY = "";
	public static int ONE = 1;
	public static String REPORT_PATH = "/../Reports";
	public static String REPO_PATH = "cloned-repos";
	public static String REPO_SUFFIX = "/.git";
	public static String BRANCH_PREFIX = "refs/heads/";
	public static String REMOTE_ORIGIN = "origin/";

	//Test file constants
	public static String REMOTE_BRANCH = "mavenization";
	public static String REMOTE_COMMIT = "48c3f6de5121a5bb156aa510279edc1ead814ca0";
	public static String BRANCH = "master";
	public static String REPO_URL = "https://github.com/fangyidong/json-simple.git";
	public static String COMMIT1 = "2f4b7b5bed38d7518bf9c6a902ea909226910ae3";
	public static String COMMIT2 = "f8d7a7570829ee93653d4ef4aeaf2d0c5e94a818";
	public static String COMMIT3 = "56d6479909872e6e65d0c1a09de147b5a8c66403";
	public static String COMMIT4 = "218acc599db1cba686791c468e1ce0df186b6f8b";
	public static String COMMIT5 = "a8b94b79b697df64b23428c27d65d6a187e9ebf9";
	public static String USER1 = "Yidong Fang";
	public static String USER2 = "darthspectrum";
	public static String REPO_URL_ALLCOMMITS = "https://github.com/hergin/JsonParsing.git";
	public static int TOTAL_COMMITS_1 = 4;
	public static int TOTAL_COMMITS_2 = 2;
	public static int ZERO = 0;
	public static String LOCALHOST = "localhost";
	public static int PORT = 8000;
	public static int HTTP_STATUS = 200;
	public static String ONE_COMMIT_URL = "/onecommit/getanalysis";
	public static String TREND_URL = "/trend/getanalysis";
	public static String HOTSPOT_URL = "/hotspot/getanalysis";
	public static String ANALYSIS_RESPONSE = "{\"Architecture Smells\":{\r\n"
			+ "      \"total_smells\": 151,\r\n"
			+ "      \"smell_distribution\":{\r\n"
			+ "         \"Cyclic Dependency\":59,\r\n"
			+ "         \"Feature Concentration\":50\r\n"
			+ "      },\r\n"
			+ "      \"top_entities\":{\r\n"
			+ "         \"input||org.apache.maven\":16,\r\n"
			+ "         \"input||org.apache.maven.model.building\":14,\r\n"
			+ "         \"input||org.apache.maven.artifact\":9,\r\n"
			+ "         \"input||org.apache.maven.model\":6\r\n"
			+ "      }\r\n"
			+ "   },\r\n"
			+ "   \"Design Smells\":{\r\n"
			+ "      \"total_smells\":891,\r\n"
			+ "      \"smell_distribution\":{\r\n"
			+ "         \"Unutilized Abstraction\":593,\r\n"
			+ "         \"Broken Hierarchy\":83,\r\n"
			+ "         \"Insufficient Modularization\":51,\r\n"
			+ "         \"Deficient Encapsulation\":51,\r\n"
			+ "         \"Feature Envy\":42\r\n"
			+ "      },\r\n"
			+ "      \"top_entities\":{\r\n"
			+ "         \"input||org.apache.maven.cli||MavenCliTest\":16,\r\n"
			+ "         \"input||org.apache.maven.repository.legacy||DefaultUpdateCheckManagerTest\":6,\r\n"
			+ "         \"input||org.apache.maven.artifact.repository.metadata||ArtifactRepositoryMetadata\":3\r\n"
			+ "      }\r\n"
			+ "   }\r\n"
			+ "}";
}
