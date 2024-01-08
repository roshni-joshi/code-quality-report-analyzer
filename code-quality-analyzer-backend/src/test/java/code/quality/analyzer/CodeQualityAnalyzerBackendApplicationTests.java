package code.quality.analyzer;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

@SpringBootTest
class CodeQualityAnalyzerBackendApplicationTests {
    @Test
    void main() {
        assertDoesNotThrow(() -> CodeQualityAnalyzerBackendApplication.main(new String[]{}));
    }
}
