"""
古代青楼舞女剧本完整处理流程演示
展示从原始剧本到最终分镜提示词的全过程
"""

import json
from consistency_checker_standalone import ConsistencyChecker


# ============================================================================
# 模拟 LLM 调用
# ============================================================================

class CourtesanDemoLLM:
    """青楼舞女剧本处理专用 LLM"""

    def __init__(self):
        self.call_count = 0

    def __call__(self, prompt: str) -> str:
        self.call_count += 1

        # 1. 剧本精简
        if "精简" in prompt or "压缩" in prompt:
            return """长安醉春楼，十五岁柳如烟被卖入青楼。她苦练舞技，初次登台一舞惊人，成为头牌红袖。穷书生萧云轩每日来看她跳舞，两人暗生情愫。权贵王爷欲强抢，萧云轩挺身而出，原来他是新科状元。萧云轩赎她出楼，两人成婚。多年后柳如烟开舞馆救助苦命女子，夫妻恩爱圆满。"""

        # 2. 一致性检查
        elif "一致性" in prompt or "角色混淆" in prompt:
            return json.dumps({
                "has_issues": False,
                "issues": [],
                "summary": "未发现角色混淆问题。主要角色柳如烟、萧云轩、李翠娘称呼一致，无代词指代混乱。"
            }, ensure_ascii=False)

        # 3. 智能分镜
        elif "分镜" in prompt or "镜头" in prompt:
            return json.dumps({
                "shots": [
                    {
                        "index": 1,
                        "start_line": 1,
                        "end_line": 5,
                        "shot_name": "初入青楼",
                        "script_excerpt": "长安城醉春楼内，十五岁的柳如烟被卖入青楼，妈妈李翠娘打量着她。",
                        "time_of_day": "夜"
                    },
                    {
                        "index": 2,
                        "start_line": 6,
                        "end_line": 10,
                        "shot_name": "苦练舞技",
                        "script_excerpt": "深夜，柳如烟独自在空荡的舞厅练习，教习妈妈春桃指导她。",
                        "time_of_day": "夜"
                    },
                    {
                        "index": 3,
                        "start_line": 11,
                        "end_line": 15,
                        "shot_name": "初次登台",
                        "script_excerpt": "醉春楼大厅宾客满座，柳如烟穿着红色舞衣登台，李翠娘冷眼旁观。",
                        "time_of_day": "夜"
                    },
                    {
                        "index": 4,
                        "start_line": 16,
                        "end_line": 20,
                        "shot_name": "一舞惊人",
                        "script_excerpt": "柳如烟舞姿如惊鸿，全场爆发掌声，青年公子萧云轩惊艳。",
                        "time_of_day": "夜"
                    },
                    {
                        "index": 5,
                        "start_line": 21,
                        "end_line": 25,
                        "shot_name": "才子相遇",
                        "script_excerpt": "后院花园，萧云轩发现柳如烟不能说话，两人初次交流。",
                        "time_of_day": "夜"
                    },
                    {
                        "index": 6,
                        "start_line": 26,
                        "end_line": 30,
                        "shot_name": "暗生情愫",
                        "script_excerpt": "萧云轩每日来看柳如烟跳舞，教她识字，两人心意相通。",
                        "time_of_day": "日"
                    },
                    {
                        "index": 7,
                        "start_line": 31,
                        "end_line": 35,
                        "shot_name": "恶客欺凌",
                        "script_excerpt": "权贵王爷看中柳如烟要强行带走，萧云轩挺身而出。",
                        "time_of_day": "夜"
                    },
                    {
                        "index": 8,
                        "start_line": 36,
                        "end_line": 40,
                        "shot_name": "英雄救美",
                        "script_excerpt": "萧云轩被打，柳如烟护他，老者揭露萧云轩是新科状元。",
                        "time_of_day": "夜"
                    },
                    {
                        "index": 9,
                        "start_line": 41,
                        "end_line": 45,
                        "shot_name": "赎身离楼",
                        "script_excerpt": "萧云轩拿出三千两银子赎柳如烟的身，李翠娘不敢再为难。",
                        "time_of_day": "日"
                    },
                    {
                        "index": 10,
                        "start_line": 46,
                        "end_line": 50,
                        "shot_name": "重获自由",
                        "script_excerpt": "柳如烟离开青楼，萧云轩牵她的手，两人携手走向新生活。",
                        "time_of_day": "日"
                    },
                    {
                        "index": 11,
                        "start_line": 51,
                        "end_line": 55,
                        "shot_name": "婚后恩爱",
                        "script_excerpt": "萧府内，柳如烟成为萧夫人，夫妻琴瑟和鸣。",
                        "time_of_day": "日"
                    },
                    {
                        "index": 12,
                        "start_line": 56,
                        "end_line": 60,
                        "shot_name": "对峙老鸨",
                        "script_excerpt": "李翠娘登门索要利息，萧云轩拿出状书对峙，老鸨灰溜溜离开。",
                        "time_of_day": "日"
                    },
                    {
                        "index": 13,
                        "start_line": 61,
                        "end_line": 65,
                        "shot_name": "宫廷献舞",
                        "script_excerpt": "柳如烟在金銮殿献舞，皇上龙颜大悦，萧云轩在殿下骄傲。",
                        "time_of_day": "日"
                    },
                    {
                        "index": 14,
                        "start_line": 66,
                        "end_line": 70,
                        "shot_name": "圆满结局",
                        "script_excerpt": "多年后柳如烟开舞馆救助女子，终于能说话，夫妻恩爱如初。",
                        "time_of_day": "日"
                    }
                ],
                "total_shots": 14,
                "notes": "全剧14个镜头，涵盖从入楼到圆满的完整故事线"
            }, ensure_ascii=False)

        return "默认响应"


# ============================================================================
# 完整处理流程
# ============================================================================

def process_courtesan_script():
    """处理青楼舞女剧本的完整流程"""

    print("=" * 80)
    print("《红袖香》- 古代青楼舞女剧本完整处理流程")
    print("=" * 80)
    print()

    # 读取原始剧本
    with open('/home/ubuntu/jellyfish-headless/test_script_courtesan.txt', 'r', encoding='utf-8') as f:
        original_script = f.read()

    print("【步骤1: 原始剧本】")
    print("=" * 80)
    print(f"字符数: {len(original_script)}")
    print(f"行数: {len(original_script.splitlines())}")
    print()
    print("剧本预览（前500字符）:")
    print("-" * 80)
    print(original_script[:500] + "...")
    print("-" * 80)
    print()

    # 初始化 LLM
    llm = CourtesanDemoLLM()

    # 步骤2: 剧本精简
    print("\n" + "=" * 80)
    print("【步骤2: 剧本精简】")
    print("=" * 80)
    simplified_prompt = f"请精简以下剧本，保留核心剧情：\n\n{original_script}"
    simplified_script = llm(simplified_prompt)

    print(f"原始字符数: {len(original_script)}")
    print(f"精简后字符数: {len(simplified_script)}")
    print(f"压缩率: {(1 - len(simplified_script) / len(original_script)) * 100:.1f}%")
    print()
    print("精简后剧本:")
    print("-" * 80)
    print(simplified_script)
    print("-" * 80)
    print()

    # 步骤3: 一致性检查
    print("\n" + "=" * 80)
    print("【步骤3: 一致性检查】")
    print("=" * 80)
    checker = ConsistencyChecker()
    consistency_result = checker.check(simplified_script, llm)

    print(f"发现问题: {'是' if consistency_result.has_issues else '否'}")
    print(f"问题数量: {len(consistency_result.issues)}")
    if consistency_result.summary:
        print(f"总结: {consistency_result.summary}")
    print()

    # 步骤4: 智能分镜
    print("\n" + "=" * 80)
    print("【步骤4: 智能分镜】")
    print("=" * 80)
    division_prompt = f"请将以下剧本分割为多个镜头：\n\n{simplified_script}"
    division_response = llm(division_prompt)
    division_result = json.loads(division_response)

    print(f"总镜头数: {division_result['total_shots']}")
    print(f"备注: {division_result.get('notes', '无')}")
    print()
    print("分镜列表:")
    print("-" * 80)
    for shot in division_result['shots']:
        print(f"镜头 {shot['index']}: {shot['shot_name']}")
        print(f"  时间: {shot['time_of_day']}")
        print(f"  内容: {shot['script_excerpt']}")
        print()
    print("-" * 80)
    print()

    # 步骤5: 生成分镜提示词
    print("\n" + "=" * 80)
    print("【步骤5: 生成分镜提示词（用于AI视频生成）】")
    print("=" * 80)
    print()

    shot_prompts = generate_shot_prompts(division_result['shots'])

    for i, prompt_data in enumerate(shot_prompts, 1):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"镜头 {i}: {prompt_data['shot_name']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print()
        print(f"【镜头类型】: {prompt_data['shot_type']}")
        print(f"【时间】: {prompt_data['time_of_day']}")
        print(f"【时长】: {prompt_data['duration']}秒")
        print()
        print(f"【视频生成提示词】")
        print("-" * 80)
        print(prompt_data['video_prompt'])
        print("-" * 80)
        print()
        print(f"【首帧提示词】")
        print("-" * 80)
        print(prompt_data['first_frame_prompt'])
        print("-" * 80)
        print()
        print(f"【尾帧提示词】")
        print("-" * 80)
        print(prompt_data['last_frame_prompt'])
        print("-" * 80)
        print()
        print(f"【镜头语言】")
        print(f"  景别: {prompt_data['shot_size']}")
        print(f"  角度: {prompt_data['camera_angle']}")
        print(f"  运镜: {prompt_data['camera_movement']}")
        print(f"  情绪: {prompt_data['emotion']}")
        print()
        print(f"【技术参数】")
        print(f"  分辨率: {prompt_data['resolution']}")
        print(f"  帧率: {prompt_data['fps']} fps")
        print(f"  风格: {prompt_data['style']}")
        print()

    # 总结
    print("\n" + "=" * 80)
    print("【处理流程总结】")
    print("=" * 80)
    print()
    print(f"✅ 原始剧本: {len(original_script)} 字符")
    print(f"✅ 精简后: {len(simplified_script)} 字符 (压缩 {(1 - len(simplified_script) / len(original_script)) * 100:.1f}%)")
    print(f"✅ 一致性检查: {'通过' if not consistency_result.has_issues else '发现问题'}")
    print(f"✅ 生成镜头数: {division_result['total_shots']} 个")
    print(f"✅ LLM 调用次数: {llm.call_count} 次")
    print()
    print("=" * 80)
    print("处理完成！所有分镜提示词已生成，可直接用于AI视频生成。")
    print("=" * 80)


def generate_shot_prompts(shots):
    """为每个镜头生成详细的AI视频生成提示词"""

    shot_prompts = []

    for shot in shots:
        prompt_data = {
            "shot_name": shot['shot_name'],
            "shot_type": determine_shot_type(shot['shot_name']),
            "time_of_day": shot['time_of_day'],
            "duration": determine_duration(shot['shot_name']),
            "video_prompt": generate_video_prompt(shot),
            "first_frame_prompt": generate_first_frame_prompt(shot),
            "last_frame_prompt": generate_last_frame_prompt(shot),
            "shot_size": determine_shot_size(shot['shot_name']),
            "camera_angle": determine_camera_angle(shot['shot_name']),
            "camera_movement": determine_camera_movement(shot['shot_name']),
            "emotion": determine_emotion(shot['shot_name']),
            "resolution": "720x1280",  # 竖屏
            "fps": 24,
            "style": "古装剧，电影质感，柔和光线"
        }
        shot_prompts.append(prompt_data)

    return shot_prompts


def determine_shot_type(shot_name):
    """根据镜头名称确定镜头类型"""
    if "登台" in shot_name or "献舞" in shot_name:
        return "表演镜头"
    elif "相遇" in shot_name or "情愫" in shot_name:
        return "情感镜头"
    elif "欺凌" in shot_name or "救美" in shot_name:
        return "冲突镜头"
    elif "结局" in shot_name or "圆满" in shot_name:
        return "结尾镜头"
    else:
        return "叙事镜头"


def determine_duration(shot_name):
    """根据镜头名称确定时长"""
    if "登台" in shot_name or "献舞" in shot_name:
        return 8  # 表演镜头较长
    elif "相遇" in shot_name or "情愫" in shot_name:
        return 6  # 情感镜头中等
    elif "欺凌" in shot_name or "救美" in shot_name:
        return 5  # 冲突镜头紧凑
    else:
        return 5  # 默认5秒


def generate_video_prompt(shot):
    """生成视频提示词"""
    base_style = "古装剧风格，电影质感，柔和光线，细腻画面"

    prompts = {
        "初入青楼": f"长安城夜晚，华丽的青楼内部，灯火通明，红色灯笼高挂。十五岁少女柳如烟穿着素色衣裙站在后院，神情惶恐。中年妇人李翠娘打量着她，眼神精明。{base_style}",

        "苦练舞技": f"深夜空荡的舞厅，月光透过窗棂洒进来。少女柳如烟独自练习舞蹈，动作生涩但坚定。汗水浸透衣衫，她咬牙坚持。教习妈妈春桃在旁指导。{base_style}",

        "初次登台": f"醉春楼大厅，宾客满座，觥筹交错。柳如烟穿着红色舞衣站在舞台中央，神情紧张。台下李翠娘冷眼旁观。灯光聚焦在舞台上。{base_style}",

        "一舞惊人": f"柳如烟翩翩起舞，红色舞衣飘逸，舞姿如惊鸿游龙。台下宾客目瞪口呆，青年公子萧云轩眼中满是惊艳。全场寂静，只有音乐声。{base_style}",

        "才子相遇": f"后院花园，月色朦胧，花香四溢。柳如烟独自落泪，萧云轩走近。两人初次交流，柳如烟用手语比划，萧云轩惊讶又怜惜。{base_style}",

        "暗生情愫": f"白天的醉春楼，阳光透过窗户。萧云轩教柳如烟识字，她用舞蹈回应他的诗词。两人相视而笑，眼中满是情意。{base_style}",

        "恶客欺凌": f"醉春楼大厅，权贵王爷气势汹汹，要强行带走柳如烟。柳如烟拼命挣扎，被打倒在地。萧云轩冲进来挡在她面前。紧张激烈的氛围。{base_style}",

        "英雄救美": f"萧云轩被侍卫打得遍体鳞伤，柳如烟哭着扑过去护住他。老者出现揭露萧云轩是新科状元，王爷脸色大变。戏剧性转折。{base_style}",

        "赎身离楼": f"白天的醉春楼，萧云轩拿出银票，李翠娘眼中闪过贪婪。柳如烟站在一旁，眼中满是希望。阳光照进来，象征新生。{base_style}",

        "重获自由": f"醉春楼门外，柳如烟终于走出青楼。萧云轩牵着她的手，两人相视而笑。阳光洒在他们身上，背景是长安城的街道。{base_style}",

        "婚后恩爱": f"萧府内，古色古香的书房和庭院。柳如烟在院中练舞，萧云轩在书房读书，时常抬头看她。温馨和谐的氛围。{base_style}",

        "对峙老鸨": f"萧府大厅，李翠娘登门索要钱财。萧云轩拿出状书，义正言辞。李翠娘恼羞成怒但无可奈何，最终灰溜溜离开。{base_style}",

        "宫廷献舞": f"金銮殿内，金碧辉煌，皇上高坐龙椅。柳如烟在殿上翩翩起舞，舞姿绝美。萧云轩在殿下看着妻子，眼中满是骄傲。庄严华丽。{base_style}",

        "圆满结局": f"多年后的舞馆，柳如烟教授舞蹈，学生们认真练习。萧云轩走进来，两人相视而笑。柳如烟开口说话：'相公，我爱你。'温馨圆满。{base_style}"
    }

    return prompts.get(shot['shot_name'], f"{shot['script_excerpt']}。{base_style}")


def generate_first_frame_prompt(shot):
    """生成首帧提示词"""
    first_frames = {
        "初入青楼": "青楼后院全景，灯火通明，柳如烟站在中央，低头不语",
        "苦练舞技": "空荡舞厅，月光洒进，柳如烟独自站立准备练习",
        "初次登台": "舞台中央，柳如烟穿红色舞衣，紧张站立，台下宾客满座",
        "一舞惊人": "柳如烟舞蹈起势，红衣飘扬，优美姿态",
        "才子相遇": "花园月下，柳如烟独自落泪，背影孤独",
        "暗生情愫": "书房内，萧云轩教柳如烟识字，两人并肩而坐",
        "恶客欺凌": "大厅内，王爷气势汹汹走向柳如烟",
        "英雄救美": "萧云轩挡在柳如烟面前，坚定的背影",
        "赎身离楼": "萧云轩拿出银票，李翠娘眼中闪过贪婪",
        "重获自由": "醉春楼门外，柳如烟回望青楼，眼中复杂",
        "婚后恩爱": "萧府庭院，柳如烟在院中起舞",
        "对峙老鸨": "萧府大厅，李翠娘登门，气势汹汹",
        "宫廷献舞": "金銮殿全景，柳如烟站在殿中央准备献舞",
        "圆满结局": "舞馆内，柳如烟教授学生，认真专注"
    }

    return first_frames.get(shot['shot_name'], shot['script_excerpt'])


def generate_last_frame_prompt(shot):
    """生成尾帧提示词"""
    last_frames = {
        "初入青楼": "柳如烟低头，眼中含泪，李翠娘冷笑",
        "苦练舞技": "柳如烟汗水浸透衣衫，但眼神坚定",
        "初次登台": "柳如烟闭眼，深呼吸，准备起舞",
        "一舞惊人": "全场起立鼓掌，萧云轩眼中惊艳",
        "才子相遇": "萧云轩和柳如烟相视，眼中情意",
        "暗生情愫": "两人相视而笑，心意相通",
        "恶客欺凌": "萧云轩挡在柳如烟面前，坚定不移",
        "英雄救美": "王爷脸色大变，灰溜溜离开",
        "赎身离楼": "李翠娘收下银票，柳如烟眼中希望",
        "重获自由": "两人携手走向远方，背影温馨",
        "婚后恩爱": "萧云轩和柳如烟相视而笑，恩爱有加",
        "对峙老鸨": "李翠娘灰溜溜离开，柳如烟感激看着萧云轩",
        "宫廷献舞": "皇上龙颜大悦，萧云轩眼中骄傲",
        "圆满结局": "萧云轩和柳如烟拥抱，热泪盈眶"
    }

    return last_frames.get(shot['shot_name'], shot['script_excerpt'])


def determine_shot_size(shot_name):
    """确定景别"""
    if "登台" in shot_name or "献舞" in shot_name:
        return "全景"
    elif "相遇" in shot_name or "情愫" in shot_name:
        return "中景"
    elif "欺凌" in shot_name or "救美" in shot_name:
        return "近景"
    else:
        return "中景"


def determine_camera_angle(shot_name):
    """确定角度"""
    if "登台" in shot_name or "献舞" in shot_name:
        return "平视"
    elif "欺凌" in shot_name:
        return "俯视"
    elif "救美" in shot_name:
        return "仰视"
    else:
        return "平视"


def determine_camera_movement(shot_name):
    """确定运镜"""
    if "登台" in shot_name or "献舞" in shot_name:
        return "环绕"
    elif "相遇" in shot_name or "情愫" in shot_name:
        return "推进"
    elif "欺凌" in shot_name or "救美" in shot_name:
        return "快速推进"
    else:
        return "静止"


def determine_emotion(shot_name):
    """确定情绪"""
    emotions = {
        "初入青楼": "惶恐、无助",
        "苦练舞技": "坚定、倔强",
        "初次登台": "紧张、恐惧",
        "一舞惊人": "惊艳、震撼",
        "才子相遇": "哀伤、温柔",
        "暗生情愫": "甜蜜、羞涩",
        "恶客欺凌": "愤怒、恐惧",
        "英雄救美": "紧张、感动",
        "赎身离楼": "希望、感激",
        "重获自由": "喜悦、解脱",
        "婚后恩爱": "温馨、幸福",
        "对峙老鸨": "愤怒、正义",
        "宫廷献舞": "庄严、骄傲",
        "圆满结局": "幸福、圆满"
    }

    return emotions.get(shot_name, "平静")


if __name__ == "__main__":
    process_courtesan_script()
