# ─── 景品設定 ─────────────────────────────────────────────────────
# weight: 確率の重み（合計100にしてある）
# coupon_url: 当たった人に表示するURL（後で設定）

PRIZES = [
    {
        "id":          "jackpot",
        "name":        "大当たり",
        "description": "【デカ盛りチャレンジ出場】\nスタッフにお声がけください。",
        "weight":      10,
        "coupon_url":  "",
        "color":       "#FF4500",
        "emoji":       "",
        "image":       "/static/dekamori.jpg",
    },
    {
        "id":          "hit",
        "name":        "あたり",
        "description": "【1キロからあげ弁当】",
        "weight":      5,
        "coupon_url":  "",
        "color":       "#FFD700",
        "emoji":       "",
        "image":       "/static/hit.jpg",
    },
    {
        "id":          "participation",
        "name":        "参加賞",
        "description": "【からあげ弁当】",
        "weight":      50,
        "coupon_url":  "",
        "color":       "#4CAF50",
        "emoji":       "",
        "image":       "/static/karaage.jpg",
    },
    {
        "id":          "lose",
        "name":        "ハズレ",
        "description": "【からあげ3個】",
        "weight":      35,
        "coupon_url":  "",
        "color":       "#9E9E9E",
        "emoji":       "",
        "image":       "/static/lose.jpg",
    },
]
