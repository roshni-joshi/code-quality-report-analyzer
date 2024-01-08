package code.quality.analyzer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.PropertySource;

@ComponentScan(basePackages = {"code.quality.analyzer"})
@PropertySource("classpath:application.properties")
@SpringBootApplication
public class CodeQualityAnalyzerBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(CodeQualityAnalyzerBackendApplication.class, args);
	}

}
