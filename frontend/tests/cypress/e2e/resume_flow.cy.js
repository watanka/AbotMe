// frontend/tests/cypress/e2e/resume_flow.cy.js
// 이력서 업로드 E2E (통합) 테스트: Cypress
// 백엔드 서버가 http://localhost:8000 에 떠 있어야 하며, 프론트엔드는 http://localhost:3000 기준

describe('이력서 업로드 통합 플로우', () => {
    it('업로드 후 ResumeViewer로 전환된다', () => {
        cy.visit('http://localhost:3000');

        // 1. 업로드 버튼 노출 및 클릭
        cy.contains('이력서 업로드').click();

        // 2. 업로드 폼 입력
        cy.get('input[aria-label="이름"]').type('홍길동');
        cy.get('input[aria-label="이메일"]').type('test@example.com');
        // PDF 샘플 파일을 cypress/fixtures/sample.pdf 위치에 준비해야 함
        cy.get('input[type="file"]').selectFile('cypress/fixtures/sample.pdf', { force: true });

        // 3. 업로드 버튼 클릭
        cy.contains('업로드').click();

        // 4. 업로드 성공 후 ResumeViewer로 전환 확인 (PDF url, 이름 등)
        cy.contains('업로드 성공').should('exist');
        cy.get('canvas').should('exist'); // react-pdf가 렌더링하는 canvas
    });
});
