// Bridgewater x Metaculus 2026 Questions
// Based on your forecasting folders

const questions = [
    {
        id: 1,
        title: "Will the X algorithm be run by Grok before March 12, 2026?",
        questionId: "41310", // You'll need to update these with actual Metaculus question IDs
        category: "tech",
        closes: "2026-02-28",
        myForecast: "12%",
        community: "5%",
        folder: "BW2026_Q01_X_GROK_ALGORITHM"
    },
    {
        id: 2,
        title: "Will the US impose new sanctions on Russia citing Ukraine before March 14, 2026?",
        questionId: "41332",
        category: "geopolitics",
        closes: "2026-03-14",
        myForecast: "86%",
        community: "~85%",
        folder: "BW2026_Q02_US_SANCTIONS_RUSSIA_UKRAINE"
    },
    {
        id: 3,
        title: "Will layoffs.fyi report ≥100 AI industry layoffs (Jan 12 - Mar 13, 2026)?",
        questionId: "41316",
        category: "tech",
        closes: "2026-02-28",
        myForecast: "32%",
        community: "38%",
        folder: "BW2026_Q03_AT_LEAST_100_TECH_LAYOFFS"
    },
    {
        id: 4,
        title: "Will the US impose any new import restriction upon China before March 14, 2026?",
        questionId: "41302",
        category: "geopolitics",
        closes: "2026-03-14",
        myForecast: "42%",
        community: "38%",
        folder: "BW2026_Q04_WILL_THE_US_IMPOSE_IMPORT_RESTRICTIONS_ON_CHINA"
    },
    {
        id: 5,
        title: "Will NVIDIA GPUs better than H200 be allowed to be exported to China before March 14, 2026?",
        questionId: "41343",
        category: "tech",
        closes: "2026-03-14",
        myForecast: "5%",
        community: "7%",
        folder: "BW2026_Q05_NVIDIA_SELL_GPUS_BETTER_THAN_H2000_TO_CHINA?"
    },
    {
        id: 6,
        title: "What percentage of US households will watch Super Bowl LX?",
        questionId: "41235",
        category: "tech",
        closes: "2026-03-14",
        myForecast: "5%",
        community: "7%",
        folder: "BW2026_Q05_NVIDIA_SELL_GPUS_BETTER_THAN_H2000_TO_CHINA?"
    },
    {
        id: 7,
        title: "Which country will lead the 2026 Winter Olympics medal table?",
        questionId: "41323",
        category: "entertainment",
        closes: "2026-02-06",
        myForecast: "Norway 64%",
        community: "Norway ~60%",
        folder: "BW2026_Q07_WINTER_OLYMPICS_MEDAL_TABLE"
    },
    {
        id: 8,
        title: "Will OpenAI API token prices fall before March 14, 2026?",
        questionId: "41336",
        category: "tech",
        closes: "2026-02-28",
        myForecast: "14%",
        community: "15%",
        folder: "BW2026_Q08_OPENAI_PRICING"
    },
    {
        id: 9,
        title: "What will be the US Manufacturing PMI in February 2026?",
        questionId: "41328",
        category: "economics",
        closes: "2026-03-03",
        myForecast: "TBD",
        community: "TBD",
        folder: "BW2026_Q09_US_MANUFACTURING_PMI_FEB_2026"
    },
    {
        id: 10,
        title: "What will be ASML's China revenue share in Q4 2025?",
        questionId: "41309",
        category: "economics",
        closes: "2026-01-29",
        myForecast: "TBD",
        community: "TBD",
        folder: "BW2026_Q10_ASML_CHINA_SHARE_Q4_2025"
    },
    {
        id: 11,
        title: "What will be the total hyperscaler capex in Q4 2025?",
        questionId: "41333",
        category: "tech",
        closes: "2026-02-28",
        myForecast: "TBD",
        community: "TBD",
        folder: "BW2026_Q11_HYPERSCALER_CAPEX_Q4_2025"
    },
    {
        id: 12,
        title: "Will any US electric utility announce a $5B+ capex increase citing datacenter demand?",
        questionId: "41356",
        category: "economics",
        closes: "2026-02-28",
        myForecast: "73%",
        community: "~75%",
        folder: "BW2026_Q12_WILL_ANY_U.S_ELECTRIC_UTILITY_ANNOUNCE_A_5BILLION_CAPEX_INCREASE_CITING_DATACENTER_DEMAND"
    },
    {
        id: 13,
        title: "Which video game will win the Grammy for Best Score Soundtrack?",
        questionId: "41331",
        category: "entertainment",
        closes: "2026-02-01",
        myForecast: "Indiana Jones 33%",
        community: "Mixed",
        folder: "BW2026_Q13_WHICH_VIDEO_GAME_WILL_WIN_A_GRAMMY_FOR_BEST_SCORE_SOUNDTRACK"
    },
    {
        id: 14,
        title: "What will be the Indian Wholesale Price Index inflation rate in January 2026?",
        questionId: "41236",
        category: "economics",
        closes: "2026-02-15",
        myForecast: "0.15% (median)",
        community: "~0.3%",
        folder: "BW2026_Q14_WHAT_WILL_BE_THE_INDIAN_WHOLESALE_PRICE_INDEX_INFLATION_RATE_IN_JANUARY_2026"
    },
    {
        id: 15,
        title: "S&P 500 conditional on payrolls",
        questionId: "41348",
        category: "economics",
        closes: "2026-02-07",
        myForecast: "TBD",
        community: "TBD",
        folder: "BW2026_Q15_SP500_CONDITIONAL_ON_PAYROLLS"
    }
];

// Calculate days remaining
function calculateDaysRemaining() {
    const endDate = new Date('2026-03-13');
    const today = new Date();
    const diffTime = Math.abs(endDate - today);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}
