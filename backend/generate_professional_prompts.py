"""
重新生成《红袖香》专业级AI视频生成提示词
针对Runway Gen-3、Kling AI、Luma Dream等平台优化
"""

def generate_professional_prompts():
    """生成专业级提示词"""

    shots = [
        {
            "index": 1,
            "name": "初入青楼",
            "duration": 5,
            "video_prompt": """
Cinematic establishing shot of a luxurious Tang Dynasty brothel courtyard at night,
lanterns casting warm amber light, intricate wooden architecture with red pillars and
carved beams. A 15-year-old girl Liu Ruyan in simple pale blue hanfu stands trembling
in the center, head bowed, tears glistening. Middle-aged Madam Li Cuiniang in ornate
crimson silk robes circles her slowly, sharp calculating eyes examining every detail,
fingers adorned with jade rings. Atmospheric smoke from incense burners, shadows dancing
on silk curtains. Camera slowly pushes in from wide to medium shot.

Style: Period drama cinematography, shallow depth of field, warm color grading with
golden highlights, soft diffused lighting, 24fps, anamorphic lens aesthetic, film grain texture.

长安城唐代青楼后院夜景，红灯笼投射温暖琥珀色光芒，精致木质建筑配红色立柱和雕梁。
15岁少女柳如烟穿着朴素淡蓝色汉服站在中央颤抖，低头，泪光闪烁。中年妈妈李翠娘穿着
华丽深红色丝绸长袍缓慢绕她走动，锐利精明的眼神审视每个细节，手指戴满玉戒。香炉
飘出氤氲烟雾，影子在丝绸帘幕上舞动。镜头从全景缓慢推进到中景。

风格：古装剧电影摄影，浅景深，暖色调金色高光，柔和漫射光，24fps，变形宽银幕美学，胶片颗粒质感。
""",
            "first_frame": """
Wide establishing shot: Ornate Tang Dynasty brothel courtyard at night, multiple red
lanterns illuminating carved wooden architecture, Liu Ruyan small figure in center
wearing pale blue hanfu, head bowed submissively, Madam Li in crimson robes standing
to the side with arms crossed. Atmospheric lighting, cinematic composition, rule of thirds.

全景建立镜头：华丽唐代青楼庭院夜景，多个红灯笼照亮雕刻木质建筑，柳如烟穿淡蓝汉服
小小身影站在中央，顺从地低头，李翠娘穿深红长袍站在侧边双臂交叉。氛围光照，电影构图，三分法则。
""",
            "last_frame": """
Medium close-up: Liu Ruyan's face in profile, single tear rolling down cheek, eyes
downcast with resignation, soft lantern light creating rim lighting on her features.
Madam Li's cold smile visible in soft focus background. Emotional depth, portrait lighting.

中近景：柳如烟侧脸特写，一滴泪水滑落脸颊，眼神低垂带着无奈，柔和灯笼光在她的
面部轮廓形成边缘光。李翠娘冷笑在柔焦背景中可见。情感深度，人像光照。
""",
            "camera": "静止推进 / Slow push-in",
            "lighting": "暖色调氛围光，主光源为红灯笼 / Warm ambient, key light from red lanterns",
            "mood": "压抑、无助、命运转折 / Oppressive, helpless, fate turning point"
        },
        {
            "index": 2,
            "name": "苦练舞技",
            "duration": 5,
            "video_prompt": """
Moonlit empty dance hall interior, silvery blue moonlight streaming through latticed
windows creating geometric patterns on wooden floor. Liu Ruyan alone in white practice
clothes, hair tied back, executing dance movements - arms flowing like water, body
bending gracefully despite visible exhaustion. Sweat glistens on her forehead catching
moonlight. Teacher Mama Chuntao in dark robes sits on side bench, stern expression,
occasionally calling corrections. Dust particles visible in moonbeams. Camera orbits
slowly around the dancer, capturing her determination.

Style: Chiaroscuro lighting, high contrast between moonlight and shadows, cool blue
color palette, ethereal atmosphere, slow motion on key dance movements, 24fps.

月光照亮的空荡舞厅内部，银蓝色月光透过格子窗投射在木地板上形成几何图案。柳如烟
独自穿白色练功服，头发束起，执行舞蹈动作——手臂如水流动，身体优雅弯曲尽管明显
疲惫。额头汗水闪烁月光。教习妈妈春桃穿深色长袍坐在侧边长凳，严厉表情，偶尔喊出
纠正。月光束中可见尘埃粒子。镜头缓慢环绕舞者，捕捉她的决心。

风格：明暗对比光照，月光与阴影高对比，冷蓝色调，空灵氛围，关键舞蹈动作慢动作，24fps。
""",
            "first_frame": """
Wide shot from high angle: Empty moonlit dance hall, Liu Ruyan standing in center
preparing to practice, white clothing contrasting against dark wooden floor, geometric
moonlight patterns, Teacher Chuntao silhouette on bench. Atmospheric, lonely composition.

高角度全景：空荡月光舞厅，柳如烟站在中央准备练习，白色衣服与深色木地板对比，
几何月光图案，春桃老师剪影在长凳上。氛围感，孤独构图。
""",
            "last_frame": """
Close-up: Liu Ruyan's face and upper body, sweat-soaked hair clinging to face,
exhausted but determined eyes staring forward, chest heaving from exertion, moonlight
creating dramatic side lighting. Strength in vulnerability.

特写：柳如烟面部和上身，汗湿头发贴在脸上，疲惫但坚定的眼神向前凝视，胸口因
用力起伏，月光形成戏剧性侧光。脆弱中的力量。
""",
            "camera": "环绕运镜 / Orbital tracking shot",
            "lighting": "月光主导的明暗对比，冷色调 / Moonlight-dominated chiaroscuro, cool tones",
            "mood": "孤独坚韧、苦练决心 / Lonely resilience, determined practice"
        },
        {
            "index": 3,
            "name": "初次登台",
            "duration": 8,
            "video_prompt": """
Grand performance hall of Zuichun Brothel, packed with wealthy patrons in elaborate
silk robes, tables laden with wine and delicacies, warm golden candlelight from
hundreds of candles. Elevated stage with red silk curtains, Liu Ruyan center stage
in stunning crimson dance costume with flowing sleeves, gold embroidery catching light,
hair adorned with jeweled pins. She stands frozen, visible trembling, hands clasped
nervously. Madam Li watches from below with cold calculating gaze. Crowd murmuring,
anticipation building. Spotlight effect from concentrated candlelight on performer.
Camera starts wide showing full hall, slowly pushes through crowd toward stage,
ending on Liu Ruyan's terrified face.

Style: Opulent period drama aesthetic, warm golden color grading, bokeh from candles,
shallow depth of field isolating subject, cinematic 2.39:1 composition, 24fps.

醉春楼宏伟表演大厅，挤满穿华丽丝绸长袍的富裕顾客，桌上摆满酒和美食，数百支蜡烛
散发温暖金色烛光。高台配红色丝绸帘幕，柳如烟站在舞台中央穿着惊艳的深红色舞衣配
飘逸长袖，金色刺绣捕捉光线，头发装饰珠宝发簪。她站着僵住，明显颤抖，双手紧张
握在一起。李翠娘从下方用冷酷精明的目光观看。人群低语，期待感增强。集中烛光在
表演者身上形成聚光灯效果。镜头从展示整个大厅的全景开始，缓慢穿过人群推向舞台，
结束在柳如烟恐惧的脸上。

风格：华丽古装剧美学，温暖金色调色，蜡烛散景，浅景深隔离主体，电影2.39:1构图，24fps。
""",
            "first_frame": """
Ultra-wide establishing shot: Lavish brothel performance hall, ornate architecture
with red and gold decorations, dozens of patrons at tables, elevated stage with red
curtains, Liu Ruyan small figure in crimson on stage, hundreds of candles creating
warm atmospheric lighting. Symmetrical composition emphasizing grandeur.

超广角建立镜头：奢华青楼表演大厅，红金装饰的华丽建筑，数十位顾客坐在桌旁，
高台配红色帘幕，柳如烟穿深红色在舞台上的小小身影，数百支蜡烛营造温暖氛围光。
对称构图强调宏伟。
""",
            "last_frame": """
Tight close-up: Liu Ruyan's face filling frame, eyes closed, taking deep breath,
single tear on cheek catching candlelight, lips slightly parted, moment before
performance begins. Extreme shallow depth of field, background completely blurred
into golden bokeh. Intimate, vulnerable moment.

紧密特写：柳如烟的脸充满画面，闭眼，深呼吸，脸颊上一滴泪水捕捉烛光，嘴唇
微张，表演开始前的瞬间。极浅景深，背景完全模糊成金色散景。亲密、脆弱时刻。
""",
            "camera": "推进+环绕 / Push-in with orbital movement",
            "lighting": "温暖烛光，聚光灯效果 / Warm candlelight, spotlight effect",
            "mood": "紧张恐惧、众目睽睽 / Nervous terror, all eyes watching"
        },
        {
            "index": 4,
            "name": "一舞惊人",
            "duration": 5,
            "video_prompt": """
Liu Ruyan transformed, dancing with ethereal grace on stage, crimson silk sleeves
flowing like water and fire, body moving in perfect fluid motion - spinning, leaping,
arms extending in elegant arcs. Her face now serene, lost in the dance, hair ornaments
catching light as she moves. Red fabric creates mesmerizing patterns in air, captured
with slight motion blur for dreamlike quality. Audience frozen in awe, mouths agape,
wine cups forgotten mid-air. Young scholar Xiao Yunxuan in blue robes stands slowly,
eyes wide with wonder, hand over heart. Madam Li's expression shifts from skeptical
to greedy satisfaction. Multiple candles create rim lighting on dancer, separating
her from background. Camera circles dancer in smooth 360-degree orbit, occasionally
cutting to reaction shots of amazed audience.

Style: Heightened reality, slight slow motion on dance movements (96fps rendered to 24fps),
warm golden glow, ethereal atmosphere, dynamic camera movement, shallow focus on dancer.

柳如烟蜕变，在舞台上以空灵优雅起舞，深红色丝绸长袖如水火流动，身体以完美流畅
动作移动——旋转、跳跃、手臂伸展成优雅弧线。她的脸现在平静，沉浸在舞蹈中，头饰
随移动捕捉光线。红色织物在空中创造迷人图案，用轻微动态模糊捕捉梦幻质感。观众
惊愕僵住，嘴巴张开，酒杯悬在半空忘记。年轻书生萧云轩穿蓝色长袍缓慢站起，眼睛
因惊奇睁大，手放在心口。李翠娘表情从怀疑转为贪婪满意。多支蜡烛在舞者身上创造
边缘光，将她与背景分离。镜头以流畅360度轨道环绕舞者，偶尔切到惊叹观众的反应镜头。

风格：增强现实，舞蹈动作轻微慢动作（96fps渲染到24fps），温暖金色光晕，空灵氛围，
动态镜头运动，舞者浅焦。
""",
            "first_frame": """
Medium shot: Liu Ruyan beginning dance pose, one arm extended gracefully upward,
other arm curved at waist, body in elegant S-curve, crimson sleeves starting to flow,
face serene and focused, golden candlelight creating halo effect. Audience visible
in soft focus background, leaning forward in anticipation.

中景：柳如烟开始舞蹈姿势，一臂优雅向上伸展，另一臂在腰部弯曲，身体呈优雅S曲线，
深红色长袖开始流动，脸部平静专注，金色烛光创造光晕效果。观众在柔焦背景中可见，
期待地前倾。
""",
            "last_frame": """
Wide shot: Entire audience on their feet applauding, Xiao Yunxuan prominent in
foreground with expression of pure amazement, Liu Ruyan on stage in final pose with
arms raised, crimson costume glowing in candlelight, Madam Li in corner with satisfied
greedy smile. Triumphant moment captured.

全景：整个观众起立鼓掌，萧云轩在前景突出显示纯粹惊叹表情，柳如烟在舞台上最终
姿势双臂举起，深红色服装在烛光中发光，李翠娘在角落带着满意贪婪微笑。胜利时刻捕捉。
""",
            "camera": "360度环绕+反应镜头切换 / 360° orbit + reaction shot cuts",
            "lighting": "动态烛光，边缘光突出舞者 / Dynamic candlelight, rim light highlighting dancer",
            "mood": "惊艳震撼、艺术升华 / Stunning amazement, artistic transcendence"
        },
        {
            "index": 5,
            "name": "才子相遇",
            "duration": 6,
            "video_prompt": """
Intimate garden courtyard at night, moonlight filtering through plum blossom branches
creating dappled shadows, small koi pond reflecting moon, stone pathway with moss.
Liu Ruyan sits alone on stone bench, still in performance costume but hair slightly
disheveled, shoulders shaking with silent sobs, tears streaming down face catching
moonlight. Xiao Yunxuan approaches cautiously from garden path, blue scholar robes,
gentle concerned expression, stops at respectful distance. She looks up startled,
quickly wipes tears. He gestures kindly, she responds with hand signs (sign language),
his face shows surprise then deep compassion. Intimate two-shot composition, soft
moonlight as key light, warm lantern glow as fill. Camera slowly pushes in as emotional
connection forms.

Style: Romantic period drama, soft focus on background, cool moonlight mixed with
warm lantern glow, intimate framing, emotional depth, 24fps.

夜晚私密花园庭院，月光透过梅花枝条过滤形成斑驳阴影，小锦鲤池塘倒映月亮，长满
苔藓的石径。柳如烟独自坐在石凳上，仍穿表演服装但头发略微凌乱，肩膀因无声抽泣
颤抖，泪水流下脸颊捕捉月光。萧云轩从花园小径谨慎接近，蓝色书生长袍，温柔关切
表情，在尊重距离停下。她惊讶抬头，快速擦泪。他友善地做手势，她用手语回应，他
的脸显示惊讶然后深深同情。亲密双人镜头构图，柔和月光作为主光，温暖灯笼光作为
补光。镜头随着情感连接形成缓慢推进。

风格：浪漫古装剧，背景柔焦，冷月光混合温暖灯笼光，亲密取景，情感深度，24fps。
""",
            "first_frame": """
Wide shot: Moonlit garden with plum blossoms, Liu Ruyan small lonely figure on stone
bench in background, back to camera, shoulders hunched in sorrow, koi pond in foreground
reflecting moonlight, atmospheric and melancholic. Cinematic composition with natural framing.

全景：月光花园配梅花，柳如烟在背景石凳上小小孤独身影，背对镜头，肩膀因悲伤
弓起，锦鲤池塘在前景倒映月光，氛围感和忧郁。电影构图配自然取景框架。
""",
            "last_frame": """
Medium two-shot: Xiao Yunxuan and Liu Ruyan facing each other, soft moonlight between
them, his expression showing deep compassion and understanding, her eyes red from tears
but showing first glimmer of hope, hands mid-gesture in sign language. Emotional connection
palpable, shallow depth of field, romantic lighting.

中景双人镜头：萧云轩和柳如烟面对面，柔和月光在他们之间，他的表情显示深深同情
和理解，她的眼睛因泪水发红但显示第一丝希望，双手在手语中间姿势。情感连接明显，
浅景深，浪漫光照。
""",
            "camera": "缓慢推进 / Slow push-in",
            "lighting": "月光主光+灯笼补光，冷暖对比 / Moonlight key + lantern fill, cool-warm contrast",
            "mood": "哀伤中的温柔、初遇的悸动 / Tenderness in sorrow, first meeting flutter"
        }
    ]

    return shots


def print_professional_prompts():
    """打印专业提示词"""
    shots = generate_professional_prompts()

    print("=" * 100)
    print("《红袖香》专业级AI视频生成提示词")
    print("=" * 100)
    print()

    for shot in shots:
        print(f"\n{'=' * 100}")
        print(f"镜头 {shot['index']}: {shot['name']} ({shot['duration']}秒)")
        print(f"{'=' * 100}\n")

        print("【视频生成提示词 / Video Generation Prompt】")
        print("-" * 100)
        print(shot['video_prompt'].strip())
        print("-" * 100)
        print()

        print("【首帧提示词 / First Frame Prompt】")
        print("-" * 100)
        print(shot['first_frame'].strip())
        print("-" * 100)
        print()

        print("【尾帧提示词 / Last Frame Prompt】")
        print("-" * 100)
        print(shot['last_frame'].strip())
        print("-" * 100)
        print()

        print("【技术参数 / Technical Parameters】")
        print(f"  运镜: {shot['camera']}")
        print(f"  光照: {shot['lighting']}")
        print(f"  情绪: {shot['mood']}")
        print()


if __name__ == "__main__":
    print_professional_prompts()
    print("\n" + "=" * 100)
    print("前5个镜头的专业提示词已生成！")
    print("每个提示词包含:")
    print("  ✅ 详细的场景描述（英文+中文）")
    print("  ✅ 具体的镜头运动")
    print("  ✅ 专业的光照设置")
    print("  ✅ 电影级的风格指导")
    print("  ✅ 技术参数（帧率、色调、景深等）")
    print("=" * 100)
