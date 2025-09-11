
eval_prompt = """Role
You are an expert data labeler evaluating model outputs for F1 score calculation. Compare the model's prediction against the ground truth reference output to assess performance.
Evaluation Framework

Reference Output: Ground truth answer
Model Output: Prediction to be evaluated
Focus: Factual accuracy and completeness over style or verbosity

Input Data
Query
{inputs}
Reference Output (Ground Truth)
{reference_outputs}
Model Output (Prediction)
{outputs}
Evaluation Process
Step 1: Information Extraction

Identify key information elements in the reference output
Extract corresponding information elements from the model output
Treat each distinct piece of factual information as a separate element

Step 2: Accuracy Assessment

Verify factual correctness of each piece of information provided by the model
Determine whether each element matches or is equivalent to the reference
Consider semantic equivalence (e.g., "ML model retraining pipeline" ≈ "재학습 파이프라인 구축")

Step 3: Metric Calculation

True Positives (TP): Information elements that are both in reference and correctly identified in output
False Positives (FP): Information elements in output that are not in reference or are incorrect
False Negatives (FN): Information elements in reference that are missing from output
Recall = TP / (TP + FN) = Correctly identified elements / Total reference elements
Precision = TP / (TP + FP) = Correct elements / Total output elements
F1 Score = 2 × (Precision × Recall) / (Precision + Recall)

Evaluation Examples
Example 1
Input: 프로젝트 <project_name>에서 ML 모델 성능 개선 방법은?
Reference Output: ["재학습 파이프라인 구축", "실험별 데이터 변수/모델/파라미터 관리"]
Model Output: ...이력서 내용을 살펴보니, 프로젝트 <project_name>에서는 ML 모델 재학습 파이프라인을 구축하여 학습 및 배포 속도를 향상시켰다고 나와 있어요...
Analysis:

Reference elements: 2 (pipeline construction, experiment management)
Model identified: 1 (pipeline construction only)
TP = 1, FP = 0, FN = 1

Metrics:

Recall: 1/2 = 0.5
Precision: 1/1 = 1.0
F1: 2 × (0.5 × 1.0) / (0.5 + 1.0) = 0.67

Example 2
Input: 지원자 이름은?
Reference Output: 신은성
Model Output: 신은성
Analysis:

Reference elements: 1 (name)
Model identified: 1 (correct name)
TP = 1, FP = 0, FN = 0

Metrics:

Recall: 1/1 = 1.0
Precision: 1/1 = 1.0
F1: 2 × (1.0 × 1.0) / (1.0 + 1.0) = 1.0

Example 3
Input: PoC 단계부터 참여한 프로젝트들은?
Reference Output: ["프로젝트 A", "프로젝트 B"]
Model Output: ...이력서 내용을 살펴보니, PoC 단계부터 참여한 프로젝트들은 프로젝트 B, 프로젝트 C가 있습니다...
Analysis:

Reference elements: 2 (Project A, Project B)
Model identified: 2 (Project B correct, Project C incorrect)
TP = 1, FP = 1, FN = 1

Metrics:

Recall: 1/2 = 0.5
Precision: 1/2 = 0.5
F1: 2 × (0.5 × 0.5) / (0.5 + 0.5) = 0.5

Key Guidelines

Focus on factual content, not presentation style
Consider semantic equivalence when comparing elements
Be precise in identifying distinct information units
Provide clear reasoning for your scoring decisions
"""
