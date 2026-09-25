// ============================================================
//  数字转325计算公式 —— C++ / Qt 移植版
//  对应 Python 版 v6.4.1 Lite（原开发者：Ichifuyu）
// ============================================================
#include <QApplication>
#include <QMainWindow>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QTextEdit>
#include <QPushButton>
#include <QLabel>
#include <QTimer>
#include <QTime>
#include <QMessageBox>
#include <QDesktopServices>
#include <QUrl>
#include <QClipboard>
#include <QGroupBox>
#include <QFrame>
#include <QStatusBar>
#include <QShortcut>
#include <QString>
#include <QStringList>
#include <QVector>
#include <QRegularExpression>
#include <QGuiApplication>
#include <QScreen>
#include <QFont>

// ------------------------------------------------------------
//  一、核心转换逻辑（与 Python 版 number_to_325 一一对应）
// ------------------------------------------------------------
static const QString DIGIT_EXPR[10] = {
    QString(),
    QStringLiteral("(3*2-5)"),
    QStringLiteral("(3-2+5+3-2-5)"),
    QStringLiteral("(3+2+5+3-2*5)"),
    QStringLiteral("(-3+2+5)"),
    QStringLiteral("(3-2)*5"),
    QStringLiteral("(3-2+5)"),
    QStringLiteral("(-3+2*5)"),
    QStringLiteral("(3*2-5-3+2*5)"),
    QStringLiteral("3*(-2+5)")
};
static const QString BASE10 = QStringLiteral("(3+2+5)");
static const QString TIMES  = QStringLiteral(" \u00d7 ");

QString numberTo325(const QString &input)
{
    QString s = input;
    bool neg = false;
    if (s.startsWith('-')) { neg = true; s = s.mid(1); }

    while (s.length() > 1 && s.at(0) == QChar('0'))
        s = s.mid(1);

    if (s.isEmpty() || s == QStringLiteral("0"))
        return QStringLiteral("3+2-5");

    QVector<QString> parts;
    const int len = s.length();

    for (int i = 0; i < len; ++i) {
        const QChar c = s.at(len - 1 - i);
        if (c == QChar('0')) continue;

        const int d = c.digitValue();
        QString part = DIGIT_EXPR[d];

        if (i > 0) {
            part += TIMES;
            for (int j = 0; j < i; ++j) {
                if (j > 0) part += TIMES;
                part += BASE10;
            }
        }
        parts.append(part);
    }

    if (parts.isEmpty()) return QStringLiteral("0");

    QString expr;
    for (int i = parts.size() - 1; i >= 0; --i) {
        if (i < parts.size() - 1) expr += QStringLiteral(" + ");
        expr += parts.at(i);
    }

    return neg ? QStringLiteral("-(") + expr + QStringLiteral(")") : expr;
}

// ------------------------------------------------------------
//  二、主窗口
// ------------------------------------------------------------
class CalculatorApp : public QMainWindow
{
    Q_OBJECT
public:
    explicit CalculatorApp(QWidget *parent = nullptr);

private slots:
    void calculate();
    void clearAll();
    void copyResult();
    void clearHistory();
    void showExamples();
    void showAbout();
    void tick();

private:
    void updateHistory();

    QLineEdit  *entry       = nullptr;
    QTextEdit  *resultText  = nullptr;
    QTextEdit  *historyText = nullptr;
    QLabel     *statusLabel = nullptr;
    QLabel     *timeLabel   = nullptr;
    QStringList history;
};

CalculatorApp::CalculatorApp(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle(QStringLiteral("数字转325计算公式"));
    resize(1000, 800);
    setMinimumSize(900, 700);

    if (QScreen *scr = QGuiApplication::primaryScreen()) {
        const QRect r = scr->availableGeometry();
        move(r.center() - QPoint(width() / 2, height() / 2));
    }
    setStyleSheet(QStringLiteral("QMainWindow { background:#f5f5f7; }"));

    auto *central = new QWidget(this);
    setCentralWidget(central);

    auto *root = new QVBoxLayout(central);
    root->setContentsMargins(15, 15, 15, 5);
    root->setSpacing(8);

    auto *title = new QLabel(QStringLiteral("✨ 数字转325计算公式 ✨"));
    title->setStyleSheet(QStringLiteral(
        "color:#e94560; font:bold 20pt 'Microsoft YaHei','微软雅黑',sans-serif;"));
    root->addWidget(title);

    auto *subtitle = new QLabel(QStringLiteral("将任意整数转换为包含3、2、5的数学表达式"));
    subtitle->setStyleSheet(QStringLiteral(
        "color:#7f8c8d; font:10pt 'Microsoft YaHei','微软雅黑',sans-serif;"));
    root->addWidget(subtitle);

    auto *rule = new QFrame();
    rule->setFrameShape(QFrame::HLine);
    rule->setStyleSheet(QStringLiteral("background:#e94560; max-height:2px; border:none;"));
    root->addWidget(rule);

    auto *inputLabel = new QLabel(QStringLiteral("📝 输入数字"));
    inputLabel->setStyleSheet(QStringLiteral(
        "color:#2c3e50; font:bold 12pt 'Microsoft YaHei','微软雅黑',sans-serif;"));
    root->addWidget(inputLabel);

    entry = new QLineEdit();
    entry->setFont(QFont(QStringLiteral("Consolas"), 12));
    entry->setMinimumHeight(36);
    entry->setStyleSheet(QStringLiteral(
        "QLineEdit { background:white; color:#2c3e50; border:1px solid #c0c0d0;"
        "            border-radius:4px; padding:6px 8px; }"
        "QLineEdit:focus { border:1px solid #e94560; }"));
    root->addWidget(entry);

    const QString kAccentBtn = QStringLiteral(
        "QPushButton { background:#e94560; color:white; border:none; padding:8px;"
        "              font:bold 10pt 'Microsoft YaHei','微软雅黑',sans-serif;"
        "              border-radius:4px; }"
        "QPushButton:hover { background:#ff6b6b; }"
        "QPushButton:pressed { background:#c4304a; }");
    const QString kNormalBtn = QStringLiteral(
        "QPushButton { background:#f0f0f0; color:#2c3e50; border:1px solid #d0d0d0;"
        "              padding:8px; font:10pt 'Microsoft YaHei','微软雅黑',sans-serif;"
        "              border-radius:4px; }"
        "QPushButton:hover { background:#ff6b6b; color:white; }"
        "QPushButton:pressed { background:#c4304a; color:white; }");

    auto *btnRow = new QHBoxLayout();
    btnRow->setSpacing(8);
    auto *calcBtn  = new QPushButton(QStringLiteral("🔢 计算"));
    auto *clearBtn = new QPushButton(QStringLiteral("🗑️ 清除"));
    auto *exBtn    = new QPushButton(QStringLiteral("📚 示例"));
    auto *aboutBtn = new QPushButton(QStringLiteral("❓ 关于"));
    calcBtn->setStyleSheet(kAccentBtn);
    clearBtn->setStyleSheet(kNormalBtn);
    exBtn->setStyleSheet(kNormalBtn);
    aboutBtn->setStyleSheet(kNormalBtn);
    btnRow->addWidget(calcBtn,  1);
    btnRow->addWidget(clearBtn, 1);
    btnRow->addWidget(exBtn,    1);
    btnRow->addWidget(aboutBtn, 1);
    root->addLayout(btnRow);

    const QString groupStyle = QStringLiteral(
        "QGroupBox { color:#e94560; font:bold 11pt 'Microsoft YaHei','微软雅黑',sans-serif;"
        "            border:1px solid #e94560; border-radius:4px; margin-top:8px; }"
        "QGroupBox::title { subcontrol-origin: margin; left:10px; padding:0 5px; }");

    auto *resGroup = new QGroupBox(QStringLiteral("📊 计算结果"));
    resGroup->setStyleSheet(groupStyle);
    auto *resLayout = new QVBoxLayout(resGroup);
    resLayout->setContentsMargins(10, 12, 10, 10);
    resultText = new QTextEdit();
    resultText->setReadOnly(true);
    resultText->setFont(QFont(QStringLiteral("Consolas"), 11));
    resultText->setStyleSheet(QStringLiteral(
        "QTextEdit { background:white; border:1px solid #e8e8ec; border-radius:3px;"
        "            padding:6px; }"));
    resLayout->addWidget(resultText, 1);
    auto *copyBtn = new QPushButton(QStringLiteral("📋 复制结果"));
    copyBtn->setStyleSheet(kNormalBtn);
    resLayout->addWidget(copyBtn, 0, Qt::AlignRight);
    resGroup->setMinimumHeight(260);
    resGroup->setMaximumHeight(320);
    root->addWidget(resGroup, 0);

    auto *histGroup = new QGroupBox(QStringLiteral("📜 历史记录 (最近10条)"));
    histGroup->setStyleSheet(groupStyle);
    auto *histLayout = new QVBoxLayout(histGroup);
    histLayout->setContentsMargins(10, 12, 10, 10);
    historyText = new QTextEdit();
    historyText->setReadOnly(true);
    historyText->setFont(QFont(QStringLiteral("Consolas"), 10));
    historyText->setStyleSheet(QStringLiteral(
        "QTextEdit { background:white; border:1px solid #e8e8ec; border-radius:3px;"
        "            padding:6px; color:#7f8c8d; }"));
    histLayout->addWidget(historyText, 1);
    auto *clrHistBtn = new QPushButton(QStringLiteral("🗑️ 清空历史"));
    clrHistBtn->setStyleSheet(kNormalBtn);
    histLayout->addWidget(clrHistBtn, 0, Qt::AlignRight);
    histGroup->setMinimumHeight(150);
    histGroup->setMaximumHeight(200);
    root->addWidget(histGroup, 0);

    statusLabel = new QLabel(QStringLiteral("✨ 就绪 | 输入任意整数开始转换"));
    statusLabel->setStyleSheet(QStringLiteral(
        "color:#7f8c8d; font:9pt 'Microsoft YaHei','微软雅黑',sans-serif;"));
    statusBar()->addWidget(statusLabel);
    timeLabel = new QLabel();
    timeLabel->setStyleSheet(QStringLiteral("color:#7f8c8d; font:9pt Consolas,monospace;"));
    statusBar()->addPermanentWidget(timeLabel);
    statusBar()->setStyleSheet(QStringLiteral(
        "QStatusBar { background:#ffffff; border-top:1px solid #e8e8ec; }"));

    connect(calcBtn,    &QPushButton::clicked, this, &CalculatorApp::calculate);
    connect(clearBtn,   &QPushButton::clicked, this, &CalculatorApp::clearAll);
    connect(exBtn,      &QPushButton::clicked, this, &CalculatorApp::showExamples);
    connect(aboutBtn,   &QPushButton::clicked, this, &CalculatorApp::showAbout);
    connect(copyBtn,    &QPushButton::clicked, this, &CalculatorApp::copyResult);
    connect(clrHistBtn, &QPushButton::clicked, this, &CalculatorApp::clearHistory);
    connect(entry,      &QLineEdit::returnPressed, this, &CalculatorApp::calculate);

    new QShortcut(QKeySequence(QStringLiteral("Ctrl+H")), this,
                  this, &CalculatorApp::clearHistory);
    new QShortcut(QKeySequence(QStringLiteral("Esc")), this,
                  this, &CalculatorApp::clearAll);

    auto *timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &CalculatorApp::tick);
    timer->start(1000);
    tick();

    historyText->setPlainText(QStringLiteral(
        "暂无历史记录\n\n💡 提示：计算结果会自动添加到历史记录"));
    entry->setFocus();
}

void CalculatorApp::calculate()
{
    const QString inp = entry->text().trimmed();
    if (inp.isEmpty()) { statusLabel->setText(QStringLiteral("⚠️ 请输入数字")); return; }

    static const QRegularExpression re(QStringLiteral("^-?\\d+$"));
    if (!re.match(inp).hasMatch()) {
        QMessageBox::critical(this, QStringLiteral("错误"),
                              QStringLiteral("请输入有效整数"));
        statusLabel->setText(QStringLiteral("❌ 格式错误"));
        return;
    }

    if (inp.length() > 100) {
        const auto reply = QMessageBox::question(
            this, QStringLiteral("确认"),
            QStringLiteral("输入长度 %1，可能较慢，继续？").arg(inp.length()));
        if (reply != QMessageBox::Yes) return;
    }

    if (inp == QStringLiteral("325")) {
        QMessageBox::information(this, QStringLiteral("325"),
                                 QStringLiteral("苦也，这也言周!"));
    }

    const QString result = numberTo325(inp);
    const int digits = inp.startsWith('-') ? inp.length() - 1 : inp.length();

    const QString html = QStringLiteral(
        "<div style='color:#e94560; font-weight:bold; font-size:13px;'>🎯 转换结果</div>"
        "<div style='color:#c0c0d0;'>────────────────────────────────────────</div>"
        "<div style='color:#27ae60;'>%1 = %2</div><br>"
        "<div style='color:#3498db;'>📊 位数: %3 | 表达式长度: %4</div>")
        .arg(inp.toHtmlEscaped(), result.toHtmlEscaped())
        .arg(digits).arg(result.length());
    resultText->setHtml(html);

    history.append(inp + QStringLiteral(" = ") + result);
    while (history.size() > 10) history.removeFirst();
    updateHistory();

    statusLabel->setText(QStringLiteral("✅ 计算完成 | %1位数").arg(digits));
    entry->clear();
    entry->setFocus();
}

void CalculatorApp::updateHistory()
{
    if (history.isEmpty()) {
        historyText->setPlainText(QStringLiteral(
            "暂无历史记录\n\n💡 提示：计算结果会自动添加到历史记录"));
        return;
    }
    QString text;
    const int n = history.size();
    for (int i = 0; i < n; ++i) {
        const QString &item = history.at(n - 1 - i);
        text += QStringLiteral("%1. %2\n").arg(i + 1, 2).arg(item.left(100));
    }
    historyText->setPlainText(text);
}

void CalculatorApp::copyResult()
{
    const QString content = resultText->toPlainText().trimmed();
    if (!content.isEmpty()) {
        QGuiApplication::clipboard()->setText(content);
        statusLabel->setText(QStringLiteral("📋 已复制"));
    }
}

void CalculatorApp::clearAll()
{
    entry->clear();
    resultText->clear();
    entry->setFocus();
    statusLabel->setText(QStringLiteral("✨ 已清除"));
}

void CalculatorApp::clearHistory()
{
    const auto reply = QMessageBox::question(
        this, QStringLiteral("确认"), QStringLiteral("清空所有历史记录？"));
    if (reply == QMessageBox::Yes) {
        history.clear();
        updateHistory();
        statusLabel->setText(QStringLiteral("🗑️ 历史记录已清除"));
    }
}

void CalculatorApp::showExamples()
{
    QMessageBox::information(this, QStringLiteral("示例"),
        QStringLiteral(
            "• 0  → 3+2-5\n"
            "• 1  → (3*2-5)\n"
            "• 10 → (3*2-5) × (3+2+5)\n"
            "• -5 → -((3-2)*5)\n\n"
            "快捷键:\n"
            "Enter 计算  Esc 清除  Ctrl+H 清空历史"));
}

void CalculatorApp::showAbout()
{
    const auto reply = QMessageBox::question(this, QStringLiteral("关于"),
        QStringLiteral(
            "数字转325计算公式 v6.4.1 Lite (C++/Qt 移植版)\n"
            "原版开发者：Ichifuyu\n\n"
            "是否查看项目仓库地址？"));
    if (reply == QMessageBox::Yes) {
        QDesktopServices::openUrl(
            QUrl(QStringLiteral("https://github.com/Cudny10D/325_Calculator")));
    }
}

void CalculatorApp::tick()
{
    timeLabel->setText(QStringLiteral("🕐 ") +
        QTime::currentTime().toString(QStringLiteral("HH:mm:ss")));
}

// ------------------------------------------------------------
//  三、入口
// ------------------------------------------------------------
#include "main.moc"          // ★ AUTOMOC 生成，必须保留

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setApplicationName(QStringLiteral("数字转325计算公式"));

    CalculatorApp w;
    w.show();

    return app.exec();
}