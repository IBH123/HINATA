# HINATA - Hybrid ICT-Strategy Navigation & Autonomous Trading Agent

**An AI-Powered Trading System Based on Inner Circle Trader (ICT) Methodology**

[![Version](https://img.shields.io/badge/Version-1.0-blue)]()
[![Status](https://img.shields.io/badge/Status-Planning-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## 🎯 Executive Summary

**HINATA** is an intelligent trading assistant that combines Large Language Model (LLM) capabilities with ICT trading methodology to provide both command-driven execution and goal-oriented strategy planning. The system employs a ReAct (Reasoning-Action) loop architecture with specialized sub-agents for comprehensive market analysis and risk-managed trade execution.

### Key Features
- **Dual-Mode Operation**: Command-driven for specific tasks, goal-driven for strategic planning
- **ReAct Architecture**: Systematic reasoning → tool selection → action → explanation workflow
- **Specialized Sub-Agents**: Context Engineer, Pattern Detector, Decision Maker, Risk Manager, and Executor
- **9-Phase Implementation**: Progressive development from data visualization to autonomous trading
- **Multi-Asset Support**: Stocks and cryptocurrency markets with unified analysis framework
- **Security-First Design**: Comprehensive safeguards before live trading activation

---

## 🔄 Operating Modes

### Command-Driven Mode
Execute specific, single-step instructions with immediate results.
- **Use Case**: Direct analysis requests (e.g., "Scan BTC-USD daily for FVGs")
- **Response**: Discrete action execution with structured results
- **Best For**: Quick analysis, specific pattern detection, status checks

### Goal-Driven Mode
Achieve complex outcomes through multi-step planning and execution.
- **Use Case**: Strategic objectives (e.g., "Find the best swing setups this week")
- **Response**: Workflow planning, sequential tool invocation, comprehensive reporting
- **Best For**: Portfolio optimization, multi-asset screening, strategic planning

### Automatic Mode
Intelligent routing based on natural language intent detection.
- **Imperative Phrasing** → Command Mode
- **Outcome Phrasing** → Goal Mode
- **Context-Aware** → Adapts to user patterns

---

## 👥 Target Audience & Scope

### Primary Users
- **Swing Traders**: Focus on daily to weekly holding periods
- **ICT Practitioners**: Traders familiar with Smart Money Concepts
- **Risk-Conscious Investors**: Emphasis on capital preservation
- **Technical Analysts**: Price action and market structure enthusiasts

### Trading Scope
- **Markets**: Equities (US stocks) and Cryptocurrency
- **Timeframes**: Daily (primary), H4/H1 (confirmation)
- **Style**: Position/Swing trading (not day trading or HFT)
- **Methodology**: ICT concepts with systematic risk management

### Platform Strategy
- **Phase 1**: Desktop web application (Streamlit)
- **Phase 2**: API layer for programmatic access
- **Phase 3**: Mobile and CLI clients

---

## 🏗️ System Architecture

### Core Components

#### 🖥️ **Frontend Layer**
- **Technology**: Streamlit single-page application
- **Layout**: Dual-pane interface (charts/analysis + AI chat)
- **Features**: Real-time updates, interactive overlays, responsive design

#### 🤖 **Agent Orchestration Layer**
- **Framework**: LangChain-based ReAct loop implementation
- **Tool Registry**: Dynamic tool selection and invocation
- **Mode Router**: Intelligent command/goal flow management

#### 🧠 **Specialized Sub-Agents**

| Agent | Primary Function | Key Capabilities |
|-------|-----------------|------------------|
| **Context Engineer** | Context optimization | Memory management, prompt engineering, retrieval |
| **Pattern Detector** | ICT analysis | Multi-timeframe scanning, structure identification |
| **Decision Maker** | Trade signals | Confluence scoring, entry/exit planning |
| **Risk Manager** | Capital protection | Position sizing, exposure monitoring |
| **Executor** | Order management | Trade execution, status tracking |

#### 📊 **Data Infrastructure**
- **Sources**: Pluggable architecture (Yahoo Finance → Premium providers)
- **Schema**: Unified OHLCV format across all assets
- **Caching**: Local storage with intelligent refresh policies

#### 🔒 **Security & Compliance**
- **Secrets Management**: Environment variables → Secret Manager
- **Access Control**: Role-based permissions
- **Audit Trail**: Comprehensive logging and monitoring
- **Safeguards**: Kill switches, rate limiting, exposure caps

---

## 🧩 Context Engineer Sub-Agent

### Purpose
Maintain optimal context quality for efficient and accurate LLM reasoning.

### Core Responsibilities
- Build a "context contract": minimal, structured state for each step
- Summarize and compress historical data into actionable insights
- Implement retrieval systems for rules, watchlists, and analyses
- Apply guardrail heuristics to filter low-quality requests
- Manage token budgets with priority-based rotation

### Output Formats

#### Analysis Header
```
Instrument: [SYMBOL]
Timeframes: [PRIMARY/CONFIRMATION]
Bias: [BULLISH/BEARISH/NEUTRAL]
Key Levels: [SUPPORT/RESISTANCE]
Timing: [SESSION/WINDOW]
Risk State: [EXPOSURE/POSITIONS]
Objective: [CURRENT GOAL]
```

#### Decision Frame
```
Confluence Score: [X/4]
├── Structure: [✓/✗]
├── Liquidity: [✓/✗]
├── Zones: [✓/✗]
└── Timing: [✓/✗]
Risk Assessment: [NOTES]
```

---

## 📈 ICT Methodology Components

### Market Structure Analysis
- **Swing Points**: Identification of structural highs and lows
- **Break of Structure (BOS)**: Trend continuation signals
- **Change of Character (ChoCH)**: Early reversal warnings

### Liquidity Concepts
- **Buy-Side Liquidity (BSL)**: Stop clusters above highs
- **Sell-Side Liquidity (SSL)**: Stop clusters below lows
- **Inducement**: Fake breakouts to trap retail traders
- **Stop Raids**: Liquidity grabs before directional moves

### Price Action Zones
- **Order Blocks**: Last opposing candle before displacement
- **Fair Value Gaps (FVG)**: Three-candle price imbalances
- **Breaker Blocks**: Failed order blocks turned resistance/support
- **Mitigation Blocks**: Zones where smart money mitigates positions

### Premium & Discount Analysis
- **Equilibrium**: 50% retracement level
- **Premium Zone**: Above equilibrium (selling area)
- **Discount Zone**: Below equilibrium (buying area)
- **Optimal Trade Entry (OTE)**: 62-79% Fibonacci zone

### Time-Based Filters
- **Kill Zones**: High-probability reversal windows
- **Session Analysis**: London, New York, Asia characteristics
- **Weekly Profiles**: Monday expansion, Wednesday reversal patterns
- **Power of Three**: Accumulation → Manipulation → Distribution

> **Note**: Pure price action approach; indicators used only for confirmation.

---

## 📋 Data Contracts & Interfaces

### Pattern Detector I/O

**Input Schema**
```json
{
  "instrument": "string",
  "timeframe": "string",
  "candles": [{
    "timestamp": "ISO8601",
    "open": "float",
    "high": "float",
    "low": "float",
    "close": "float",
    "volume": "float"
  }]
}
```

**Output Schema**
```json
{
  "structure": {
    "bias": "BULLISH|BEARISH|NEUTRAL",
    "last_bos": {"timestamp": "ISO8601", "price": "float"},
    "last_choch": {"timestamp": "ISO8601", "price": "float"}
  },
  "liquidity": {
    "bsl": [{"price": "float", "distance": "float"}],
    "ssl": [{"price": "float", "distance": "float"}],
    "recent_sweeps": []
  },
  "zones": {
    "order_blocks": [{"range": ["float", "float"], "type": "string"}],
    "fvgs": [{"range": ["float", "float"], "filled": "boolean"}]
  }
}
```

---

## 🎨 User Interface Design

### Layout Structure

```
┌──────────────────────────────────────────────────────┐
│                    HINATA Trading System             │
├────────────┬──────────────────────┬──────────────────┤
│            │                      │                   │
│  Controls  │    Chart Display     │   AI Assistant   │
│            │                      │                   │
│ • Symbol   │  • Candlesticks      │  • Chat Interface│
│ • Timeframe│  • ICT Overlays      │  • Mode Toggle   │
│ • Overlays │  • Entry/Exit Points │  • Signal Cards  │
│ • Simulator│  • Risk Zones        │  • Risk Alerts   │
│            │                      │                   │
└────────────┴──────────────────────┴──────────────────┘
```

### Component Details

#### Left Panel - Control Center
- Symbol search and selection
- Timeframe quick toggles (D, H4, H1)
- Overlay management (OB, FVG, Liquidity, Structure)
- Simulator controls and settings

#### Center Panel - Chart Visualization
- Interactive candlestick chart
- ICT markup overlays with tooltips
- Entry/exit visualization
- Risk/reward projection

#### Right Panel - AI Assistant
- Mode selector (Auto/Command/Goal)
- Conversational interface
- Signal cards with rationale
- Risk management alerts
- Performance metrics

---

## 📅 Implementation Roadmap

### Phase 1: Data Foundation & Visualization
**Timeline**: Weeks 1-2

#### Objectives
- Establish robust data pipeline for historical OHLCV
- Create foundational charting infrastructure
- Implement basic UI framework

#### Deliverables
- ✅ Data fetching module (Yahoo Finance API)
- ✅ Candlestick chart rendering
- ✅ Symbol/timeframe selection UI
- ✅ Basic overlay toggle interface

#### Success Metrics
- Load 1 year daily + 3 months H4 data
- Support minimum 3 instruments
- Sub-second chart rendering

### Phase 2: AI Assistant Core
**Timeline**: Weeks 3-4

#### Objectives
- Implement ReAct loop architecture
- Deploy Context Engineer sub-agent
- Establish tool registry and routing

#### Deliverables
- ✅ Chat interface with mode selection
- ✅ Command/Goal routing logic
- ✅ Context Engineer implementation
- ✅ Tool registry with basic tools

### Phase 3: ICT Pattern Detection Engine
**Timeline**: Weeks 5-7

#### Objectives
- Build comprehensive ICT pattern detection
- Implement multi-timeframe analysis
- Create quality scoring algorithms

#### Deliverables
- ✅ Market structure analyzer
- ✅ Liquidity pool mapper
- ✅ Order block detector
- ✅ Fair value gap scanner
- ✅ Premium/discount calculator

### Phase 4: Testing & Validation Framework
**Timeline**: Weeks 8-9

#### Objectives
- Comprehensive testing infrastructure
- Backtesting framework development
- Performance benchmarking

#### Deliverables
- ✅ Unit test suite (>80% coverage)
- ✅ Integration testing framework
- ✅ Backtesting engine
- ✅ Performance metrics dashboard

### Phase 5: Decision Engine & Visualization
**Timeline**: Weeks 10-11

#### Objectives
- Implement confluence-based decision logic
- Create comprehensive visualization layer
- Build notification system

#### Deliverables
- ✅ Confluence scoring algorithm
- ✅ Signal generation engine
- ✅ Visual overlay system
- ✅ Notification framework

### Phase 6: Risk Management System
**Timeline**: Weeks 12-13

#### Objectives
- Comprehensive risk management framework
- Portfolio analytics and monitoring
- Proactive risk alerts

#### Deliverables
- ✅ Position sizing calculator
- ✅ Portfolio exposure tracker
- ✅ Correlation analyzer
- ✅ Drawdown protection

### Phase 7: Trading Simulator
**Timeline**: Weeks 14-15

#### Objectives
- Full-featured paper trading system
- Performance analytics suite
- Scenario testing capabilities

#### Deliverables
- ✅ Paper trading engine
- ✅ PnL calculator with slippage
- ✅ Equity curve visualization
- ✅ Performance metrics

### Phase 8: Security & Live Trading
**Timeline**: Weeks 16-18

#### Objectives
- Production-grade security implementation
- Live trading infrastructure
- Comprehensive safeguards

#### Deliverables
- ✅ Secret management system
- ✅ Authentication & authorization
- ✅ Kill switch implementation
- ✅ Robinhood API integration

### Phase 9: Advanced AI/ML Enhancement
**Timeline**: Weeks 19-20+

#### Objectives
- ML-enhanced pattern recognition
- Reinforcement learning optimization
- Cross-platform expansion

#### Deliverables
- ✅ ML quality scoring models
- ✅ RL parameter optimization
- ✅ RAG knowledge base
- ✅ Multi-asset scanner
- ✅ API backend service

---

## 🛡️ Governance, Safety & Compliance

### Safety Protocols

#### Human-in-the-Loop Controls
- ✅ Mandatory confirmation for live trades
- ✅ Dry-run preview before execution
- ✅ Override capability at all stages

#### Risk Policy Gates
- **Daily Loss Limit**: Configurable max daily drawdown
- **Position Limits**: Max concurrent positions
- **Exposure Caps**: Per-asset and total portfolio
- **Time Filters**: Weekend, earnings, news blackouts
- **Correlation Limits**: Max correlated exposure

#### Audit & Compliance
- **Comprehensive Logging**: All decisions and actions
- **PII Protection**: Automatic redaction
- **Regulatory Compliance**: Trade reporting capabilities
- **Data Retention**: Configurable retention policies

#### System Resilience
- **Module Isolation**: Independent component operation
- **Graceful Degradation**: Fallback to simpler modes
- **Circuit Breakers**: Automatic halt conditions
- **Rollback Capability**: Version control for configs

---

## 🚀 Cross-Platform Expansion

### Architecture Evolution

```
Phase 1: Monolithic Web App
┌─────────────────┐
│  Streamlit App  │
│  (Frontend +    │
│   Backend)      │
└─────────────────┘

Phase 2: API Separation
┌─────────────────┐     ┌─────────────────┐
│  Streamlit UI   │────▶│   REST API      │
└─────────────────┘     │   Backend       │
                        └─────────────────┘

Phase 3: Multi-Client
┌─────────────────┐
│   Web Client    │────┐
└─────────────────┘    │
┌─────────────────┐    ├───▶┌─────────────────┐
│  Mobile Client  │────┤    │   Unified API   │
└─────────────────┘    │    │   Backend       │
┌─────────────────┐    │    └─────────────────┘
│   CLI Client    │────┘
└─────────────────┘
```

---

## ✅ Implementation Checklist

### Project Setup
- [ ] Initialize Git repository with .gitignore
- [ ] Create project structure (src/, tests/, docs/, config/)
- [ ] Set up development environment
- [ ] Configure linting and formatting
- [ ] Establish CI/CD pipeline

### Phase Execution
- [ ] **Phase 1**: Data pipeline and visualization
- [ ] **Phase 2**: AI assistant and ReAct loop
- [ ] **Phase 3**: ICT pattern detection
- [ ] **Phase 4**: Testing and validation
- [ ] **Phase 5**: Decision engine and UI
- [ ] **Phase 6**: Risk management
- [ ] **Phase 7**: Trading simulator
- [ ] **Phase 8**: Security and live trading
- [ ] **Phase 9**: ML enhancements

### Quality Assurance
- [ ] Code review process established
- [ ] Test coverage >80%
- [ ] Documentation complete
- [ ] Security audit passed
- [ ] Performance benchmarks met

### Deployment
- [ ] Staging environment configured
- [ ] Production deployment plan
- [ ] Monitoring and alerting setup
- [ ] Disaster recovery plan
- [ ] User onboarding materials

---

## 💬 Interaction Examples

### Command Mode Examples

```
User: "Scan AAPL daily for FVGs"
HINATA: Found 3 unfilled FVGs:
  • Bullish FVG: $145.20-$146.80 (2 days old)
  • Bearish FVG: $152.10-$152.90 (5 days old)
  • Bullish FVG: $141.00-$142.30 (7 days old)
```

```
User: "Show BTC liquidity sweeps this week"
HINATA: Liquidity sweep analysis:
  • Monday: BSL sweep at $45,200 → Reversal
  • Wednesday: SSL sweep at $42,800 → Continuation
  • Friday: BSL raid at $44,500 → ChoCH formed
```

### Goal Mode Examples

```
User: "Find the best swing setups in my watchlist"
HINATA: Analyzing 10 instruments across multiple timeframes...

Top 3 Setups:
1. NVDA - Long Setup (Confidence: 85%)
   • Entry: $420-425 (Daily OB)
   • Stop: $415 (Below SSL)
   • Targets: $435, $445
   • Confluence: Bullish structure + Discount zone + FVG support

2. BTC/USD - Short Setup (Confidence: 78%)
   • Entry: $44,800-45,200 (H4 Breaker)
   • Stop: $45,800 (Above BSL)
   • Targets: $43,000, $41,500
   • Confluence: Bearish ChoCH + Premium zone + Liquidity void

3. AAPL - Long Setup (Confidence: 72%)
   • Entry: $178-179 (Daily FVG CE)
   • Stop: $176.50 (Structure low)
   • Targets: $183, $186
   • Confluence: Bullish bias + OTE zone + Session timing
```

### Risk Management Dialogue

```
User: "How's my risk looking?"
HINATA: Portfolio Risk Analysis:
  • Current Exposure: 18% of capital
  • Open Positions: 3 (2 longs, 1 short)
  • Correlation Risk: Moderate (tech sector 65%)
  • Suggested Action: Can take 1 more position at 1% risk
  • Warning: Approaching daily loss limit (currently -1.2%)
```

---

## 📚 Additional Resources

### Documentation
- [ICT Concepts Glossary](./docs/ict_glossary.md)
- [API Documentation](./docs/api.md)
- [User Guide](./docs/user_guide.md)
- [Developer Guide](./docs/developer_guide.md)

### Community
- GitHub Issues: Bug reports and feature requests
- Discord: Community discussions
- Wiki: Collaborative knowledge base

### Legal
- [Terms of Service](./legal/terms.md)
- [Privacy Policy](./legal/privacy.md)
- [Risk Disclaimer](./legal/disclaimer.md)

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**License**: MIT  
**Contributors**: Open for collaboration

---

> **Disclaimer**: This system is for educational purposes. Trading involves substantial risk. Past performance does not guarantee future results. Always conduct your own research and consider your risk tolerance before trading.