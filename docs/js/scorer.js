/**
 * scorer.js — 评分模块
 * 纯函数，无副作用，接收题目与用户答案，输出评分结果。
 */

/**
 * 对用户答卷进行评分
 *
 * @param {Object[]} questions  - 原始题目数组 (含 answer, type, options 等)
 * @param {Object}   userAnswers - 用户答案映射 { questionId: answer }
 *                                 单选 → "A" / 多选 → ["A", "C"] / 未答 → undefined
 * @returns {{
 *   total: number,
 *   correct: number,
 *   incorrect: number,
 *   unanswered: number,
 *   percentage: number,
 *   results: Object[]  // 每题详细结果
 * }}
 */
export function score(questions, userAnswers) {
  let correctCount = 0;
  let incorrectCount = 0;
  let unansweredCount = 0;

  const results = questions.map((q) => {
    const userAnswer = userAnswers[q.id];
    const isAnswered = userAnswer !== undefined && userAnswer !== null
      && (Array.isArray(userAnswer) ? userAnswer.length > 0 : true);

    if (!isAnswered) {
      unansweredCount++;
      return {
        id: q.id,
        stem: q.stem,
        type: q.type,
        options: q.options,
        correctAnswer: q.answer,
        userAnswer: null,
        isCorrect: false,
        isAnswered: false,
      };
    }

    const isCorrect = checkAnswer(userAnswer, q.answer, q.type);
    if (isCorrect) {
      correctCount++;
    } else {
      incorrectCount++;
    }

    return {
      id: q.id,
      stem: q.stem,
      type: q.type,
      options: q.options,
      correctAnswer: q.answer,
      userAnswer: userAnswer,
      isCorrect,
      isAnswered: true,
    };
  });

  const total = questions.length;
  const percentage = total > 0 ? Math.round((correctCount / total) * 100) : 0;

  return {
    total,
    correct: correctCount,
    incorrect: incorrectCount,
    unanswered: unansweredCount,
    percentage,
    results,
  };
}

/**
 * 检查用户答案是否正确
 */
function checkAnswer(userAnswer, correctAnswer, type) {
  if (type === 'multiple') {
    // 多选题：数组比较（忽略顺序）
    if (!Array.isArray(userAnswer) || !Array.isArray(correctAnswer)) return false;
    if (userAnswer.length !== correctAnswer.length) return false;
    const sortedUser = [...userAnswer].sort();
    const sortedCorrect = [...correctAnswer].sort();
    return sortedUser.every((v, i) => v === sortedCorrect[i]);
  }
  // 单选题：字符串比较
  return String(userAnswer) === String(correctAnswer);
}

/**
 * 根据百分比返回评级标签
 */
export function getGradeLabel(percentage) {
  if (percentage >= 90) return { text: '优秀', cls: 'great' };
  if (percentage >= 75) return { text: '良好', cls: 'good' };
  if (percentage >= 60) return { text: '及格', cls: 'ok' };
  return { text: '需努力', cls: 'poor' };
}

/**
 * 统计用户答题进度
 */
export function getProgress(questions, userAnswers) {
  const total = questions.length;
  const answered = questions.filter((q) => {
    const ans = userAnswers[q.id];
    return ans !== undefined && ans !== null
      && (Array.isArray(ans) ? ans.length > 0 : true);
  }).length;
  return { total, answered, percentage: total > 0 ? Math.round((answered / total) * 100) : 0 };
}
