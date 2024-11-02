import pandas as pd

# 植物数据
plants_data = [
    {"ID": 1, "名称": "向日葵", "英文名称": "Sunflower", "伤害": 0, "血量": 300, "阳光消耗": 50},
    {"ID": 2, "名称": "豌豆射手", "英文名称": "Peashooter", "伤害": 20, "血量": 300, "阳光消耗": 100},
    {"ID": 3, "名称": "双发射手", "英文名称": "Repeater", "伤害": "20 x 2", "血量": 300, "阳光消耗": 200},
    {"ID": 4, "名称": "坚果墙", "英文名称": "Wall-nut", "伤害": 0, "血量": 4000, "阳光消耗": 50},
    {"ID": 5, "名称": "土豆雷", "英文名称": "Potato Mine", "伤害": "爆炸", "血量": 300, "阳光消耗": 25},
    {"ID": 6, "名称": "樱桃炸弹", "英文名称": "Cherry Bomb", "伤害": "爆炸", "血量": 300, "阳光消耗": 150},
    {"ID": 7, "名称": "火爆辣椒", "英文名称": "Jalapeno", "伤害": "爆炸", "血量": 300, "阳光消耗": 125},
    {"ID": 8, "名称": "寒冰射手", "英文名称": "Snow Pea", "伤害": 20, "血量": 300, "阳光消耗": 175},
    {"ID": 9, "名称": "小喷菇", "英文名称": "Puff-shroom", "伤害": 20, "血量": 150, "阳光消耗": 0},
    {"ID": 10, "名称": "大喷菇", "英文名称": "Fume-shroom", "伤害": 30, "血量": 300, "阳光消耗": 75},
    {"ID": 11, "名称": "巨型坚果", "英文名称": "Tall-nut", "伤害": 0, "血量": 8000, "阳光消耗": 125},
    {"ID": 12, "名称": "三线射手", "英文名称": "Threepeater", "伤害": "20 x 3", "血量": 300, "阳光消耗": 325},
    {"ID": 13, "名称": "地刺", "英文名称": "Spikeweed", "伤害": 20, "血量": 300, "阳光消耗": 100},
    {"ID": 14, "名称": "火炬树桩", "英文名称": "Torchwood", "伤害": "增加火焰伤害", "血量": 300, "阳光消耗": 175},
    {"ID": 15, "名称": "南瓜头", "英文名称": "Pumpkin", "伤害": 0, "血量": 4000, "阳光消耗": 125},
    {"ID": 16, "名称": "双子向日葵", "英文名称": "Twin Sunflower", "伤害": 0, "血量": 300, "阳光消耗": 150},
    {"ID": 17, "名称": "毁灭菇", "英文名称": "Doom-shroom", "伤害": "爆炸", "血量": 300, "阳光消耗": 125},
    {"ID": 18, "名称": "小喷菇", "英文名称": "Scaredy-shroom", "伤害": 20, "血量": 300, "阳光消耗": 25},
    {"ID": 19, "名称": "洋葱", "英文名称": "Garlic", "伤害": 0, "血量": 400, "阳光消耗": 50},
    {"ID": 20, "名称": "大王花", "英文名称": "Gloom-shroom", "伤害": 40, "血量": 300, "阳光消耗": 150},
    {"ID": 21, "名称": "磁力菇", "英文名称": "Magnet-shroom", "伤害": "吸收金属", "血量": 300, "阳光消耗": 100},
    {"ID": 22, "名称": "翻转器", "英文名称": "Umbrella Leaf", "伤害": 0, "血量": 300, "阳光消耗": 100},
    {"ID": 23, "名称": "吃人花", "英文名称": "Chomper", "伤害": "单次吞噬", "血量": 300, "阳光消耗": 150},
    {"ID": 24, "名称": "仙人掌", "英文名称": "Cactus", "伤害": 20, "血量": 300, "阳光消耗": 125},
    {"ID": 25, "名称": "海蘑菇", "英文名称": "Sea-shroom", "伤害": 20, "血量": 150, "阳光消耗": 0},
    {"ID": 26, "名称": "高坚果", "英文名称": "Tall Wall-nut", "伤害": 0, "血量": 8000, "阳光消耗": 125},
    {"ID": 27, "名称": "大喇叭菇", "英文名称": "Blover", "伤害": 0, "血量": 300, "阳光消耗": 100},
    {"ID": 28, "名称": "玉米加农炮", "英文名称": "Cob Cannon", "伤害": "爆炸", "血量": 300, "阳光消耗": 500},
    {"ID": 29, "名称": "洋葱", "英文名称": "Garlic", "伤害": 0, "血量": 400, "阳光消耗": 50},
    {"ID": 30, "名称": "菌类控制菇", "英文名称": "Hypno-shroom", "伤害": "控制僵尸", "血量": 300, "阳光消耗": 75},
    {"ID": 31, "名称": "咖啡豆", "英文名称": "Coffee Bean", "伤害": 0, "血量": 300, "阳光消耗": 75}
]

# 僵尸数据
zombies_data = [
    {"ID": 1, "名称": "普通僵尸", "英文名称": "Zombie", "攻击力": 10, "血量": 270, "特殊能力": "无"},
    {"ID": 2, "名称": "路障僵尸", "英文名称": "Conehead Zombie", "攻击力": 10, "血量": 560,
     "特殊能力": "路障提供额外保护"},
    {"ID": 3, "名称": "铁桶僵尸", "英文名称": "Buckethead Zombie", "攻击力": 10, "血量": 1370,
     "特殊能力": "铁桶提供额外保护"},
    {"ID": 4, "名称": "撑杆僵尸", "英文名称": "Pole Vaulting Zombie", "攻击力": 10, "血量": 340,
     "特殊能力": "可以跳过第一个植物"},
    {"ID": 5, "名称": "橄榄球僵尸", "英文名称": "Football Zombie", "攻击力": 10, "血量": 1650,
     "特殊能力": "高速移动，高血量"},
    {"ID": 6, "名称": "舞王僵尸", "英文名称": "Dancing Zombie", "攻击力": 10, "血量": 340, "特殊能力": "召唤伴舞僵尸"},
    {"ID": 7, "名称": "伴舞僵尸", "英文名称": "Backup Dancer", "攻击力": 10, "血量": 200,
     "特殊能力": "跟随舞王僵尸生成"},
    {"ID": 8, "名称": "气球僵尸", "英文名称": "Balloon Zombie", "攻击力": 10, "血量": 340,
     "特殊能力": "通过气球飞越植物"},
    {"ID": 9, "名称": "投石车僵尸", "英文名称": "Catapult Zombie", "攻击力": 10, "血量": 340,
     "特殊能力": "用投石车摧毁植物"},
    {"ID": 10, "名称": "雪橇僵尸", "英文名称": "Zomboni", "攻击力": 10, "血量": 1370, "特殊能力": "铺冰道并碾压植物"},
    {"ID": 11, "名称": "海豚骑士僵尸", "英文名称": "Dolphin Rider Zombie", "攻击力": 10, "血量": 340,
     "特殊能力": "可跳跃水中植物"},
    {"ID": 12, "名称": "潜水僵尸", "英文名称": "Snorkel Zombie", "攻击力": 10, "血量": 200,
     "特殊能力": "潜水以避开攻击"},
    {"ID": 13, "名称": "跳舞僵尸", "英文名称": "Dancing Zombie", "攻击力": 10, "血量": 340, "特殊能力": "召唤伴舞僵尸"},
    {"ID": 14, "名称": "梯子僵尸", "英文名称": "Ladder Zombie", "攻击力": 10, "血量": 670,
     "特殊能力": "放置梯子以穿越障碍物"},
    {"ID": 15, "名称": "蹦极僵尸", "英文名称": "Bungee Zombie", "攻击力": 0, "血量": 340, "特殊能力": "从空中抓走植物"},
    {"ID": 16, "名称": "读报僵尸", "英文名称": "Newspaper Zombie", "攻击力": 10, "血量": 340,
     "特殊能力": "报纸破裂后速度加快"},
    {"ID": 17, "名称": "桶装僵尸", "英文名称": "Screen Door Zombie", "攻击力": 10, "血量": 560,
     "特殊能力": "屏风门提供额外保护"},
    {"ID": 18, "名称": "红眼巨人僵尸", "英文名称": "Gargantuar", "攻击力": 20, "血量": 3000,
     "特殊能力": "超高血量，抛掷小鬼僵尸"},
    {"ID": 19, "名称": "小鬼僵尸", "英文名称": "Imp Zombie", "攻击力": 10, "血量": 100, "特殊能力": "被抛掷入场"},
    {"ID": 20, "名称": "金盔僵尸", "英文名称": "Gold Head Zombie", "攻击力": 10, "血量": 1370,
     "特殊能力": "金头盔提供更高保护"},
    {"ID": 21, "名称": "僵王博士", "英文名称": "Dr. Zomboss", "攻击力": 50, "血量": 15000,
     "特殊能力": "最终Boss，使用多种攻击"}
]

# 创建DataFrame
plants_df = pd.DataFrame(plants_data)
zombies_df = pd.DataFrame(zombies_data)


class PVZDatabase:
    def __init__(self, plants_df, zombies_df):
        self.plants_df = plants_df
        self.zombies_df = zombies_df

    def search_plant(self, keyword):
        """搜索植物"""
        result = self.plants_df[
            self.plants_df['名称'].str.contains(keyword, na=False) |
            self.plants_df['英文名称'].str.contains(keyword, na=False)
            ]
        return result if not result.empty else "未找到匹配的植物"

    def search_zombie(self, keyword):
        """搜索僵尸"""
        result = self.zombies_df[
            self.zombies_df['名称'].str.contains(keyword, na=False) |
            self.zombies_df['英文名称'].str.contains(keyword, na=False)
            ]
        return result if not result.empty else "未找到匹配的僵尸"

    def get_plant_stats(self):
        """获取植物统计信息"""
        stats = {
            "总植物数量": len(self.plants_df),
            "平均阳光消耗": self.plants_df['阳光消耗'].mean(),
            "最高血量植物": self.plants_df.loc[self.plants_df['血量'].idxmax()]['名称'],
            "最贵植物": self.plants_df.loc[self.plants_df['阳光消耗'].idxmax()]['名称']
        }
        return stats

    def get_zombie_stats(self):
        """获取僵尸统计信息"""
        stats = {
            "总僵尸数量": len(self.zombies_df),
            "平均血量": self.zombies_df['血量'].mean(),
            "最高血量僵尸": self.zombies_df.loc[self.zombies_df['血量'].idxmax()]['名称'],
            "最强攻击力僵尸": self.zombies_df.loc[self.zombies_df['攻击力'].idxmax()]['名称']
        }
        return stats

    def save_data(self):
        """保存数据到文件"""
        # 保存植物数据
        self.plants_df.to_excel("plants_data.xlsx", index=False, sheet_name="植物数据")
        self.plants_df.to_csv("plants_data.csv", index=False, encoding='utf-8-sig')

        # 保存僵尸数据
        self.zombies_df.to_excel("zombies_data.xlsx", index=False, sheet_name="僵尸数据")
        self.zombies_df.to_csv("zombies_data.csv", index=False, encoding='utf-8-sig')

        # 保存完整数据到一个Excel文件的不同sheet
        with pd.ExcelWriter("pvz_complete_data.xlsx") as writer:
            self.plants_df.to_excel(writer, sheet_name="植物数据", index=False)
            self.zombies_df.to_excel(writer, sheet_name="僵尸数据", index=False)

        print("数据已保存到以下文件：")
        print("- plants_data.xlsx 和 plants_data.csv (植物数据)")
        print("- zombies_data.xlsx 和 zombies_data.csv (僵尸数据)")
        print("- pvz_complete_data.xlsx (包含所有数据)")
