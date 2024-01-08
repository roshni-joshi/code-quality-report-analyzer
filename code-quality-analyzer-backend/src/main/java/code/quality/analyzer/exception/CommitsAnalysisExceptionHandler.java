package code.quality.analyzer.exception;

import java.io.IOException;

import org.eclipse.jgit.api.errors.CheckoutConflictException;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.api.errors.InvalidRefNameException;
import org.eclipse.jgit.api.errors.RefAlreadyExistsException;
import org.eclipse.jgit.api.errors.RefNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@ControllerAdvice
public class CommitsAnalysisExceptionHandler extends ResponseEntityExceptionHandler {

	@ExceptionHandler({UnsupportedOperationException.class, IOException.class})
	public ResponseEntity<String> handleIncorrectRepoPathException(Exception exception, WebRequest request) {
		return new ResponseEntity<String>("Repository not found: " + exception.getMessage(), HttpStatus.NOT_FOUND);
	}
	
	@ExceptionHandler({ RefAlreadyExistsException.class, RefNotFoundException.class, InvalidRefNameException.class,
			CheckoutConflictException.class, GitAPIException.class })
	public ResponseEntity<String> handleInvalidBranchException(Exception exception, WebRequest request) {
		return new ResponseEntity<String>("Invalid branch name: " + exception.getMessage(), HttpStatus.NOT_FOUND);
	}
	
	@ExceptionHandler({InvalidCommitsException.class})
	public ResponseEntity<String> handleInvalidCommitsException(Exception exception, WebRequest request) {
		return new ResponseEntity<String>("Invalid commit ids: " + exception.getMessage(), HttpStatus.NOT_FOUND);
	}
}
