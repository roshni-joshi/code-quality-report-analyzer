package code.quality.analyzer.exception;

/**
 * Exception class for invalid commit ids
 */
public class InvalidCommitsException extends RuntimeException {
	private static final long serialVersionUID = 1L;

	public InvalidCommitsException() {}
	
	public InvalidCommitsException(String message) {
		super(message);
	}
}
