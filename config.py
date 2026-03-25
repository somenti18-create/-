# ─── 景品設定 ─────────────────────────────────────────────────────
# weight: 確率の重み（合計100にしてある）
# coupon_url: 当たった人に表示するURL（後で設定）

PRIZES = [
    {
        "id":          "jackpot",
        "name":        "大当たり（ハズレ）",
        "description": "デカ盛りチャレンジ出演権おめでとう！\nスタッフにお声がけください。",
        "weight":      10,
        "coupon_url":  "",   # ← 後でURLを入れる
        "color":       "#FF4500",
        "emoji":       "🎪",
    },
    {
        "id":          "hit",
        "name":        "あたり！",
        "description": "1キロからあげ弁当引換券",
        "weight":      5,
        "coupon_url":  "",   # ← 後でURLを入れる
        "color":       "#FFD700",
        "emoji":       "🏆",
    },
    {
        "id":          "participation",
        "name":        "参加賞",
        "description": "からあげ弁当1個プレゼント！",
        "weight":      50,
        "coupon_url":  "",   # ← 後でURLを入れる
        "color":       "#4CAF50",
        "emoji":       "🍱",
    },
    {
        "id":          "lose",
        "name":        "ハズレ",
        "description": "からあげ3個プレゼント！",
        "weight":      35,
        "coupon_url":  "",   # ← 後でURLを入れる
        "color":       "#9E9E9E",
        "emoji":       "🍗",
    },
]
