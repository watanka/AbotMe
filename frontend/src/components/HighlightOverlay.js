import React from "react";

/**
 * 하이라이트 오버레이 컴포넌트
 * @param {Object[]} highlights - [{x0, x1, top, bottom, page_id, ...}]
 * @param {number} pageWidth - 렌더링된 PDF 페이지 width
 * @param {number} pageHeight - 렌더링된 PDF 페이지 height
 * @param {number} pdfWidth - 원본 PDF width
 * @param {number} pdfHeight - 원본 PDF height
 */
export default function HighlightOverlay({ highlights, pageWidth, pageHeight, pdfWidth, pdfHeight }) {
    if (!Array.isArray(highlights) || !pdfWidth || !pdfHeight) return null;

    // bbox 변환 함수
    // const scaleX = pageWidth / pdfWidth;
    // const scaleY = pageHeight / pdfHeight;

    return (
        <>
            {highlights.map((bbox, i) => {
                
                if (
                    bbox == null ||
                    bbox.x0 == null || bbox.x1 == null || bbox.top == null || bbox.bottom == null
                ) return null;
                // 면적 확장 (2%)
                // PDF 원본 기준 정규화 bbox를 실제 렌더링 크기에 맞게 변환
                console.log("bbox not filtered.")
                const EXPAND = 0.02;
                let left = bbox.x0 * pageWidth;
                let top = bbox.top * pageHeight;
                let width = (bbox.x1 - bbox.x0) * pageWidth;
                let height = (bbox.bottom - bbox.top) * pageHeight;
                // 2% 확장
                left -= width * EXPAND / 2;
                top -= height * EXPAND / 2;
                width *= (1 + EXPAND);
                height *= (1 + EXPAND);
                // 디버깅용 로그 제거 또는 필요시 유지
                console.log("left:", left, "top:", top, "width:", width, "height:", height);
                return (
                    <div
                        key={i}
                        className="absolute pointer-events-none rounded-xl shadow transition-all duration-200"
                        style={{
                            left, top, width, height,
                            backgroundColor: "rgba(208, 208, 110, 0.45)",
                            boxSizing: "border-box",
                            zIndex: 10
                        }}
                    // title={hl.name || hl.tags}
                    />
                );
            })}
        </>
    );
}
