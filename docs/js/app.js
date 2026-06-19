/**
 * app.js — 主应用
 * 负责路由、数据加载、页面渲染。
 */

import { createQuizEngine } from './quiz-engine.js';
import { score, getGradeLabel, getProgress } from './scorer.js';

// ---- 科目注册 ----
const SUBJECTS = {
  scrum:  { slug: 'scrum',  title: 'Scrum 2026',  desc: 'Scrum 框架与敏捷实践',         file: 'data/scrum.json' },
  xp:     { slug: 'xp',     title: 'XP 2026',      desc: '极限编程与工程实践',             file: 'data/xp.json' },
  agile:  { slug: 'agile',  title: 'Agile 2026',   desc: '敏捷宣言、价值观与原则',        file: 'data/agile.json' },
  kanban: { slug: 'kanban', title: 'Kanban & Lean 2026', desc: '看板方法与精益思想',     file: 'data/kanban.json' },
};

// ---- 全局状态 ----
let currentQuizEngine = null;
let currentSubject = null;

// ---- DOM 引用缓存 ----
const appEl = document.getElementById('app');

// ================================================================
// ROUTER
// ================================================================

function parseRoute() {
  const hash = window.location.hash.replace(/^#/, '') || '/';
  const parts = hash.split('/').filter(Boolean);

  // /quiz/<subject>
  if (parts[0] === 'quiz' && parts[1]) {
    return { page: 'quiz', subject: parts[1] };
  }
  // /result/<subject>
  if (parts[0] === 'result' && parts[1]) {
    return { page: 'result', subject: parts[1] };
  }
  // /
  return { page: 'home' };
}

function navigate(path) {
  window.location.hash = path;
}

function onRouteChange() {
  const route = parseRoute();
  switch (route.page) {
    case 'home':
      renderHome();
      break;
    case 'quiz':
      renderQuiz(route.subject);
      break;
    case 'result':
      renderResult(route.subject);
      break;
    default:
      renderHome();
  }
}

// ================================================================
// DATA LOADING
// ================================================================

const _dataCache = {};

async function loadSubjectData(slug) {
  if (_dataCache[slug]) return _dataCache[slug];

  const subj = SUBJECTS[slug];
  if (!subj) throw new Error(`未知科目: ${slug}`);

  const resp = await fetch(subj.file);
  if (!resp.ok) throw new Error(`加载失败: ${resp.status}`);
  const data = await resp.json();
  _dataCache[slug] = data;
  return data;
}

// ================================================================
// HEADER RENDERING
// ================================================================

function renderHeader(showBack, backLabel, backPath) {
  const header = document.getElementById('site-header');
  if (!header) return;

  const backHtml = showBack
    ? `<a href="${backPath}" class="back-link" data-nav>← ${backLabel}</a>`
    : '';

  header.innerHTML = `
    <div class="container">
      <a href="#" class="logo" data-nav>课堂小测</a>
      ${backHtml}
    </div>
  `;

  // Delegate navigation clicks
  header.querySelectorAll('[data-nav]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const href = el.getAttribute('href');
      if (href === '#') navigate('/');
      else if (href) navigate(href.replace(/^#/, ''));
    });
  });
}

// ================================================================
// HOME PAGE
// ================================================================

function renderHome() {
  renderHeader(false);
  currentQuizEngine = null;
  currentSubject = null;

  const cards = Object.values(SUBJECTS).map((s) => `
    <a href="#/quiz/${s.slug}" class="subject-card" data-nav="${s.slug}">
      <div class="info">
        <h3>${s.title}</h3>
        <span>${s.desc}</span>
      </div>
      <span class="caret">→</span>
    </a>
  `).join('');

  appEl.innerHTML = `
    <div class="container">
      <div class="home-intro">
        <h1>课堂小测</h1>
        <p>敏捷软件开发 · 选择科目开始答题，每题即时反馈</p>
      </div>
      <div class="subject-list">
        ${cards}
      </div>
    </div>
  `;

  // Bind card clicks (for non-hash navigation consistency)
  appEl.querySelectorAll('.subject-card').forEach((card) => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      const slug = card.getAttribute('data-nav');
      navigate(`/quiz/${slug}`);
    });
  });
}

// ================================================================
// QUIZ PAGE
// ================================================================

async function renderQuiz(slug) {
  const subj = SUBJECTS[slug];
  if (!subj) { renderHome(); return; }

  renderHeader(true, '返回首页', '/');

  // Show loading
  appEl.innerHTML = '<div class="container"><div class="loading">加载题目中…</div></div>';

  try {
    const data = await loadSubjectData(slug);
    const engine = createQuizEngine(data.questions, { shuffle: true });
    currentQuizEngine = engine;
    currentSubject = slug;

    renderQuizUI(engine, subj);
  } catch (err) {
    appEl.innerHTML = `<div class="container"><div class="empty-state">
      <div class="emoji">⚠️</div>
      <h3>加载失败</h3>
      <p>${err.message}</p>
      <button class="btn btn-primary mt-2" onclick="window.location.reload()">重试</button>
    </div></div>`;
  }
}

function renderQuizUI(engine, subj) {
  const q = engine.getCurrentQuestion();
  if (!q) return;

  const locked = engine.isLocked(q.id);
  const progress = getProgress(engine.questions, engine.getUserAnswers());
  const lockedCount = engine.getLockedCount();

  // Sidebar dots (show locked state differently)
  const dotsHtml = engine.questions.map((tq, idx) => {
    const isLocked = engine.isLocked(tq.id);
    const current = idx === engine.currentIndex;
    let cls = 'question-dot';
    if (current) cls += ' current';
    else if (isLocked) cls += ' answered';
    return `<button class="${cls}" data-goto="${idx}" title="第${tq.id}题">${tq.id}</button>`;
  }).join('');

  // Mobile dots
  const mobileDotsHtml = engine.questions.map((tq, idx) => {
    const isLocked = engine.isLocked(tq.id);
    const current = idx === engine.currentIndex;
    let cls = 'mobile-dot';
    if (current) cls += ' current';
    else if (isLocked) cls += ' answered';
    return `<button class="${cls}" data-goto="${idx}" title="第${tq.id}题"></button>`;
  }).join('');

  // Options rendering with feedback states
  const isMulti = q.type === 'multiple';
  const inputType = isMulti ? 'checkbox' : 'radio';

  // 获取正确答案（转换为显示 key，以便与渲染的选项 key 比较）
  const qData = engine.questions.find(t => t.id === q.id);
  const correctAnswerOriginal = qData?.answer;
  const keyMap = qData?._keyMap; // original → display

  function toDisplayKeys(answer) {
    if (!answer) return null;
    if (!keyMap) return answer; // 未乱序，原样返回
    if (Array.isArray(answer)) return answer.map(k => keyMap[k] || k);
    return keyMap[answer] || answer;
  }
  const correctAnswerDisplay = toDisplayKeys(correctAnswerOriginal);

  const optionsHtml = q.options.map((opt) => {
    const isSelected = q.selectedKeys && q.selectedKeys.includes(opt.key);
    let cls = 'option-item';

    if (locked) {
      cls += ' locked';
      // 用显示 key 判断正确选项
      const isCorrectOption = (isMulti && Array.isArray(correctAnswerDisplay))
        ? correctAnswerDisplay.includes(opt.key)
        : opt.key === correctAnswerDisplay;

      if (isSelected && isCorrectOption) {
        cls += ' correct-choice';
      } else if (isSelected && !isCorrectOption) {
        cls += ' incorrect-choice';
      } else if (!isSelected && isCorrectOption) {
        cls += ' reveal-correct';
      }
    } else if (isSelected) {
      cls += ' selected';
    }

    const disabled = locked ? 'disabled' : '';
    return `
      <div class="${cls}" data-key="${opt.key}">
        <input type="${inputType}" name="question_${q.id}" value="${opt.key}"
          id="opt_${q.id}_${opt.key}" ${isSelected ? 'checked' : ''} ${disabled}>
        <span class="option-letter">${opt.key}</span>
        <label class="option-text" for="opt_${q.id}_${opt.key}">${escapeHtml(opt.text)}</label>
      </div>
    `;
  }).join('');

  // Feedback toast for locked question
  let feedbackHtml = '';
  if (locked) {
    const qData = engine.questions.find(t => t.id === q.id);
    const userAns = engine.getUserAnswers()[q.id];
    const isCorrect = checkAnswerCorrect(userAns, qData?.answer, q.type);
    if (isCorrect) {
      feedbackHtml = '<div class="feedback-toast correct">回答正确</div>';
    } else {
      const correctDisplay = formatAnswerDisplay(qData?.answer, qData?._keyMap);
      feedbackHtml = `<div class="feedback-toast incorrect">回答错误，正确答案是 <b>${correctDisplay}</b></div>`;
    }
  }

  const typeLabel = isMulti ? '多选题' : '单选题';
  const progressPct = engine.total > 0 ? Math.round((engine.currentIndex + 1) / engine.total * 100) : 0;

  // Footer: different buttons based on state
  let footerRightHtml;
  if (engine.isAllLocked()) {
    footerRightHtml = '<button class="btn btn-primary btn-lg" id="btn-view-result">查看成绩</button>';
  } else if (engine.hasNext()) {
    footerRightHtml = '<button class="btn btn-primary" id="btn-next">下一题 →</button>';
  } else {
    // On last question but not all locked yet (shouldn't normally happen, but handle gracefully)
    footerRightHtml = '<button class="btn btn-primary" id="btn-next" disabled>最后一题</button>';
  }

  // Auto-advance hint
  const statusText = locked
    ? `已答 ${lockedCount}/${progress.total}`
    : `已答 ${lockedCount}/${progress.total}`;

  appEl.innerHTML = `
    <div class="container">
      <div class="quiz-layout">
        <!-- Main quiz area -->
        <div class="quiz-main">
          <div class="quiz-card">
            <div class="quiz-progress-bar">
              <div class="fill" style="width:${progressPct}%"></div>
            </div>
            <div class="quiz-body">
              <div class="question-meta">
                <span class="question-number">第 ${q.id} 题 / 共 ${q.total} 题</span>
                <span class="question-type-badge">${typeLabel}</span>
              </div>
              <div class="question-stem">${escapeHtml(q.stem)}</div>
              <div class="options-list" role="${isMulti ? 'group' : 'radiogroup'}" aria-label="选项">
                ${optionsHtml}
              </div>
              ${feedbackHtml}
            </div>
            <div class="quiz-footer">
              <button class="btn btn-secondary" id="btn-prev" ${!engine.hasPrev() ? 'disabled' : ''}>
                ← 上一题
              </button>
              <span style="font-size:0.85rem;color:var(--color-text-muted)">
                ${statusText}
              </span>
              ${footerRightHtml}
            </div>
          </div>
          <div class="mobile-dots">${mobileDotsHtml}</div>
        </div>

        <!-- Sidebar -->
        <div class="progress-sidebar">
          <div class="inner">
            <h4>答题卡</h4>
            <div class="question-dots">${dotsHtml}</div>
            <div style="margin-top:12px;font-size:0.8rem;color:var(--color-text-muted)">
              已锁定: ${lockedCount} / ${progress.total}
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  // ---- Event bindings ----
  bindQuizEvents(engine, subj);
}

function bindQuizEvents(engine, subj) {
  const q = engine.getCurrentQuestion();
  const locked = engine.isLocked(q.id);

  // Option selection (only if not locked)
  if (!locked) {
    appEl.querySelectorAll('.option-item').forEach((item) => {
      item.addEventListener('click', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'LABEL') return;
        const key = item.getAttribute('data-key');
        if (q.type === 'multiple') {
          const checkbox = item.querySelector('input[type="checkbox"]');
          if (checkbox) {
            checkbox.checked = !checkbox.checked;
            updateMultiSelectInstant(q.id, engine);
          }
        } else {
          const radio = item.querySelector('input[type="radio"]');
          if (radio) {
            radio.checked = true;
            onOptionSelected(engine, subj, q.id, key);
          }
        }
      });
    });

    // Radio direct change
    appEl.querySelectorAll('input[type="radio"]').forEach((radio) => {
      radio.addEventListener('change', (e) => {
        onOptionSelected(engine, subj, q.id, e.target.value);
      });
    });

    // Checkbox direct change
    appEl.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
      cb.addEventListener('change', () => {
        updateMultiSelectInstant(q.id, engine);
      });
    });
  }

  // Navigation buttons
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const btnViewResult = document.getElementById('btn-view-result');

  if (btnPrev) btnPrev.addEventListener('click', () => {
    engine.prev();
    renderQuizUI(engine, subj);
  });
  if (btnNext) btnNext.addEventListener('click', () => {
    engine.next();
    renderQuizUI(engine, subj);
  });
  if (btnViewResult) btnViewResult.addEventListener('click', () => {
    window._quizResults = {
      subject: subj,
      userAnswers: engine.getUserAnswers(),
      questions: engine.questions,
    };
    navigate(`/result/${subj}`);
  });

  // Sidebar dots
  appEl.querySelectorAll('[data-goto]').forEach((dot) => {
    dot.addEventListener('click', () => {
      const idx = parseInt(dot.getAttribute('data-goto'));
      engine.goTo(idx);
      renderQuizUI(engine, subj);
    });
  });
}

/**
 * 用户选择了某个选项（单选即时反馈）
 */
function onOptionSelected(engine, subj, questionId, displayKey) {
  // 记录答案
  engine.selectAnswer(questionId, displayKey);
  // 锁定题目
  engine.lockQuestion(questionId);
  // 重新渲染以显示反馈
  renderQuizUI(engine, subj);

  // 自动跳转下一题（延迟 1 秒）
  if (!engine.isAllLocked()) {
    setTimeout(() => {
      // 找到第一个未锁定的题目并跳转
      const qs = engine.questions;
      for (let i = 0; i < qs.length; i++) {
        if (!engine.isLocked(qs[i].id)) {
          engine.goTo(i);
          renderQuizUI(engine, subj);
          return;
        }
      }
      // 全部锁定则刷新显示「查看成绩」按钮
      renderQuizUI(engine, subj);
    }, 1000);
  } else {
    // 最后一题答完，刷新显示「查看成绩」
    renderQuizUI(engine, subj);
  }
}

function updateMultiSelectInstant(questionId, engine) {
  const selected = [];
  appEl.querySelectorAll(`input[name="question_${questionId}"]:checked`).forEach((cb) => {
    selected.push(cb.value);
  });
  engine.selectAnswer(questionId, selected.length > 0 ? selected : null);
  // Visual update
  appEl.querySelectorAll('.option-item').forEach((item) => {
    const key = item.getAttribute('data-key');
    const checkbox = item.querySelector('input[type="checkbox"]');
    if (checkbox && checkbox.checked) {
      item.classList.add('selected');
    } else {
      item.classList.remove('selected');
    }
  });
}

/**
 * 检查用户答案是否正确
 */
function checkAnswerCorrect(userAnswer, correctAnswer, type) {
  if (userAnswer === undefined || userAnswer === null) return false;
  if (type === 'multiple') {
    if (!Array.isArray(userAnswer) || !Array.isArray(correctAnswer)) return false;
    if (userAnswer.length !== correctAnswer.length) return false;
    const sortedUser = [...userAnswer].sort();
    const sortedCorrect = [...correctAnswer].sort();
    return sortedUser.every((v, i) => v === sortedCorrect[i]);
  }
  return String(userAnswer) === String(correctAnswer);
}

/**
 * 格式化答案用于显示（原始 key → 显示 key）
 * @param {string|string[]} answer - 原始 key
 * @param {Object|null} keyMap - 原始 key → 显示 key 的映射表
 */
function formatAnswerDisplay(answer, keyMap) {
  if (!answer) return '?';
  if (Array.isArray(answer)) {
    return answer.map(k => keyMap ? (keyMap[k] || k) : k).join(', ');
  }
  return keyMap ? (keyMap[answer] || answer) : String(answer);
}

// ================================================================
// RESULT PAGE
// ================================================================

function renderResult(slug) {
  const data = window._quizResults;
  if (!data || data.subject !== slug) {
    // No result data — redirect to quiz
    navigate(`/quiz/${slug}`);
    return;
  }

  const subj = SUBJECTS[slug];
  renderHeader(true, '返回首页', '/');

  const scoreResult = score(data.questions, data.userAnswers);
  const grade = getGradeLabel(scoreResult.percentage);

  // Summary
  const summaryHtml = `
    <div class="result-header">
      <div class="result-score ${grade.cls}">${scoreResult.percentage}%</div>
      <div class="result-label">${grade.text}</div>
      <div class="result-stats">
        <span>正确 <b>${scoreResult.correct}</b></span>
        <span>错误 <b>${scoreResult.incorrect}</b></span>
        <span>未答 <b>${scoreResult.unanswered}</b></span>
      </div>
      <div class="result-actions">
        <button class="btn btn-outline" id="btn-retry">重新作答</button>
        <a href="#" class="btn btn-secondary" data-nav>← 返回首页</a>
      </div>
    </div>
  `;

  // Review list
  const reviewHtml = scoreResult.results.map((r, idx) => {
    const statusCls = r.isCorrect ? 'correct' : 'incorrect';
    const statusText = r.isCorrect ? '正确' : (r.isAnswered ? '错误' : '未答');

    // Find display keys for answers
    const qData = data.questions.find(q => q.id === r.id);
    const displayOpts = qData ? qData._displayOptions : r.options;
    const keyMap = qData ? qData._keyMap : null;  // original → display

    function getDisplayKey(origKey) {
      if (!keyMap) return origKey;
      return keyMap[origKey] || origKey;
    }

    function formatAnswer(ans) {
      if (!ans) return '（未作答）';
      if (Array.isArray(ans)) return ans.map(getDisplayKey).join(', ');
      return getDisplayKey(String(ans));
    }

    return `
      <div class="review-item ${statusCls}">
        <div class="review-header">
          <span class="review-number">第 ${r.id} 题</span>
          <span class="review-status">${statusText}</span>
        </div>
        <div class="review-stem">${escapeHtml(r.stem)}</div>
        <div class="review-answers">
          <span class="your-answer">你的答案: <b>${formatAnswer(r.userAnswer)}</b></span>
          ${!r.isCorrect ? `<span class="correct-answer">正确答案: <b>${formatAnswer(r.correctAnswer)}</b></span>` : ''}
        </div>
      </div>
    `;
  }).join('');

  appEl.innerHTML = `
    <div class="container">
      ${summaryHtml}
      <h2 class="mb-2">答题详情</h2>
      <div class="review-list">
        ${reviewHtml}
      </div>
    </div>
  `;

  // Event bindings
  const btnRetry = document.getElementById('btn-retry');
  if (btnRetry) {
    btnRetry.addEventListener('click', () => {
      window._quizResults = null;
      navigate(`/quiz/${slug}`);
    });
  }

  // Back to home link
  appEl.querySelectorAll('[data-nav]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      window._quizResults = null;
      navigate('/');
    });
  });
}

// ================================================================
// UTILITY
// ================================================================

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ================================================================
// INIT
// ================================================================

window.addEventListener('hashchange', onRouteChange);
window.addEventListener('DOMContentLoaded', onRouteChange);
