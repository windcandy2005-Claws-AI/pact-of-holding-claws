import os
import streamlit as st


# ==================================================
# 基本設定
# ==================================================

st.set_page_config(
    page_title="執爪之約",
    page_icon="🐾",
    layout="wide",
)

APP_NAME = "執爪之約"
ENGLISH_NAME = "Pact of Holding Claws"

DISCLAIMER = (
    "本作品提供之資訊僅供輔助參考，不能取代獸醫師之診斷、治療或專業建議。"
    "貓犬之健康與營養需求可能因個體狀況而異，"
    "如有健康疑慮或需要調整飲食與照護方式，請諮詢合格獸醫師。"
)

PRIVACY_NOTICE = (
    "請使用虛構或不具識別性的資料。不要輸入姓名、電話、地址、"
    "精確收入、真實病歷、API 金鑰或其他可識別資料。"
    "需要交接真實聯絡資訊時，可下載後自行在本機補上。"
)

AI_INSTRUCTIONS = """
你是「執爪之約」的飼養規劃整理助手。

請以繁體中文，根據使用者提供的資料及規則式清單，
整理成以下四個部分：

1. 先確認的事情
2. 可執行的小步驟
3. 需要詢問獸醫師或其他合適專業人員的事項
4. 可供使用者修改的求助或討論摘要

重要要求：
- 尊重使用者，不羞辱、不評分、不判定是否有資格飼養。
- 同時關注飼主的困難與動物的安全和照護需求。
- 不補充使用者未提供的事實，不推測疾病、行為原因或棄養風險。
- 不提供診斷、治療、用藥或具體行為矯正處方。
- 不建議任何可能造成恐懼、疼痛或傷害的方式。
- 不編造機構、補助、聯絡方式、空位、費用或資料來源。
- 不保證防逃、防墜、治療效果或避免棄養。
- 不替使用者決定是否領養、安置或轉送。
- 若使用者提到經濟或居住限制，只整理可討論的選項，不替使用者決定是否飼養。
- 缺少的資訊標示為「待確認」。
- 若確實無法繼續照顧，可建議諮詢主管機關或可信任的
  動保相關單位，了解妥善安置與交接方式；不虛構具體資源。
- 提醒使用者確認、修改後，再採用或分享。
"""


# ==================================================
# 選項與固定內容
# ==================================================

MONEY_STATUS = ["待確認", "已有準備方式", "正在評估中", "目前不允許飼養"]

MONEY_TASKS = {
    "待確認": (
        "經濟與支出：盤點日常用品、定期照護、必要醫療及緊急事件"
        "可能產生的支出，確認自己的準備方式後再決定時機。"
    ),
    "已有準備方式": (
        "經濟與支出：定期檢視日常及緊急照護的支出安排；"
        "收入變動時，先確認可以調整的項目與可討論的支持方式。"
    ),
    "正在評估中": (
        "經濟與支出：列出日常、定期與緊急支出的大約區間與資金來源，"
        "評估後再決定接回毛孩的時間，不必一次決定所有細節。"
    ),
    "目前不允許飼養": (
        "經濟與支出：目前條件若不允許，可先暫緩接回毛孩，"
        "並把需要達成的條件寫成可檢視的清單；不建議為了想養而勉強承擔超出能力的支出。"
    ),
}

CHIP_STATUS = ["待確認", "已登記且資料正確", "尚未登記或需更新"]

CHANGE_PLANS = {
    "搬家或租約到期": (
        "提前確認新住處是否允許飼養；搬家期間可規劃寵物住宿或親友暫時照護，"
        "並同步更新晶片與登記資料。"
    ),
    "工作或收入變化": (
        "重新盤點日常與緊急支出，列出可暫時調整的項目；"
        "必要時與可信任的人討論分擔照護。"
    ),
    "出差或長時間外出": (
        "事先列出不在家期間的照護工作，確認備援人選或寵物住宿等選項，"
        "並建議提前試住或實地參觀。"
    ),
    "家庭成員變化（懷孕、育兒或新同住者）": (
        "提前與同住者討論新的照護分工，並確認寵物與新成員的互動安全。"
    ),
    "寵物年齡或健康變化": (
        "提前了解高齡或慢性照護需求，整理想與獸醫師討論的問題，"
        "並評估可能增加的照護時間與費用。"
    ),
}

FAMILY_VIEWS = ["尚未詢問", "已討論且同意", "有保留意見", "明確反對"]

HOME_SAFETY_CHECKS = {
    "窗戶沒有紗窗，或紗窗可能被撐開": (
        "檢查窗戶與紗窗的固定方式，評估是否需要加裝紗窗或窗戶限位器；"
        "改善前，避免貓狗單獨接觸開啟的窗戶。"
    ),
    "陽台沒有防護網或防墜措施": (
        "評估陽台欄杆間距與防護網狀況，確認貓狗無法攀爬或擠出；"
        "改善前，陽台門保持關閉並有人陪同。"
    ),
    "大門或出入口常開": (
        "在出入口設置緩衝區或安全門，避免開門時寵物直接衝出；"
        "並讓家中每位成員都了解開門規則。"
    ),
    "窗戶開啟角度過大": (
        "使用限位器或其他固定方式限制開啟角度，並定期確認是否鬆脫。"
    ),
    "外出裝備可能鬆脫": (
        "檢查項圈、牽繩與胸背帶是否合身、扣具是否牢固；"
        "外出前確認裝備，並向專業人員了解適合個體的外出方式。"
    ),
    "家中有縫隙或圍欄缺口": (
        "檢查床底、櫃底、門縫與圍欄缺口，封閉或修補可能讓寵物鑽出的空間。"
    ),
}

FINAL_STEPS = [
    "先不要在情緒最激烈或最疲累時做不可逆的決定。",
    "先找可信任的人，討論短期寄養、分擔照護或暫時陪伴；必要時評估寵物住宿。",
    "諮詢獸醫師或具適當專業背景的人員，確認是否有健康或行為因素需要處理。",
    "若仍確定無法繼續照顧，向所在地主管機關或可信任的動保相關單位諮詢妥善安置與交接方式。",
    "交接前整理完整照護資訊，並確認接手者的意願與能力。",
]


# ==================================================
# 小工具
# ==================================================

def add_section(lines, title, items):
    lines.append("")
    lines.append(f"【{title}】")
    for item in items:
        lines.append(f"- {item}")


def safe_text(value):
    value = str(value).strip()
    return value if value else "待確認"


def format_value(value):
    if isinstance(value, list):
        return "、".join(value) if value else "尚未勾選"
    return safe_text(value)


def yes_no_pending(label, key):
    return st.selectbox(
        label,
        ["待確認", "已安排／已確認", "需要協助或調整"],
        key=key,
    )


# ==================================================
# 準飼主：依八個面向產生行動清單
# ==================================================

def preparation_tasks(data):
    tasks = []
    pet = data["動物"]

    # 1. 時間與日常照護
    if data["日常照護"] == "已安排／已確認":
        tasks.append(
            "時間與日常照護：定期檢查照護分工，並確認加班、"
            "出差或旅行時的替代安排。"
        )
    else:
        tasks.append(
            "時間與日常照護：列出餵食、清潔、陪伴、就醫及外出時段，"
            "確認誰負責，以及加班或旅行時的空缺。"
        )

    if pet in ["狗", "還沒決定"]:
        tasks.append(
            "外出與活動：依個體需求安排散步或活動時間，"
            "確認平日與突發情況下誰能協助。"
        )

    # 2. 經濟
    tasks.append(MONEY_TASKS[data["經濟準備"]])

    # 3. 居住與逃脫風險
    for item in data["居住檢查項目"]:
        tasks.append(f"{item}：{HOME_SAFETY_CHECKS[item]}")

    if not data["居住檢查項目"]:
        tasks.append(
            "居住安全：尚未勾選檢查項目。建議逐一檢查窗戶、紗窗、"
            "陽台、大門與縫隙，確認是否有可能讓寵物逃脫或墜落的風險。"
        )

    if data["不在家情形"] in ["每週 3 天以上", "經常出差或長時間外出"]:
        tasks.append(
            "不在家時間較長：先列出需要照護的工作與可信任的協助者；"
            "若尚未安排，可比較寵物住宿等短期選項，並事前試住或參觀。"
        )

    if not data["短期備案"] or "尚未規劃" in data["短期備案"]:
        tasks.append(
            "短期備案：目前尚未規劃，建議先列出兩至三個可行選項，並確認其條件與可用性。"
        )

    # 4. 寵物登記
    if data["晶片與登記"] == "已登記且資料正確":
        tasks.append(
            "寵物登記：定期確認晶片與登記資料仍正確，"
            "搬家或更換聯絡方式後記得同步更新。"
        )
    else:
        tasks.append(
            "寵物登記：向所在地主管機關確認晶片植入與登記方式、"
            "需要準備的資料；登記資料有變動時要同步更新。"
        )

    tasks.append(
        "環境安全：收納線材、清潔用品及其他可能被誤食或咬壞的物品；"
        "規劃休息、活動與避開刺激的空間。"
    )

    # 5. 租屋與搬遷
    if data["住處規定"] == "目前不允許":
        tasks.append(
            "租屋與搬遷：目前住處不允許飼養。先確認合適且允許飼養的居住安排，"
            "再決定接貓狗回家的時間。"
        )
    elif data["住處規定"] == "尚未確認":
        tasks.append(
            "租屋與搬遷：確認租約、房東及管理規約是否允許飼養；"
            "可詢問是否能將相關約定明確記錄。"
        )
    else:
        tasks.append(
            "租屋與搬遷：保存已確認的飼養約定，並思考租約到期或搬家時的居住備案。"
        )

    if data["搬遷備案"] != "已安排／已確認":
        tasks.append(
            "搬遷備案：預先想好若需要搬家或換住處，寵物的運輸、暫時照護與新住處檢查方式；若新住處無法立即入住，可考慮寵物住宿作為過渡方案。"
        )

    # 6. 家庭
    if data["家人意見"] in ["有保留意見", "明確反對"]:
        tasks.append(
            "家庭共識：先了解對方具體顧慮，例如過敏、噪音、清潔或支出，"
            "不急著說服；若仍無共識，暫緩飼養決定。"
        )
    elif data["家人意見"] == "尚未詢問":
        tasks.append(
            "家庭共識：和同住者討論意願、清潔、噪音、支出及照護分工；"
            "有兒童或對動物不自在的成員時，也要討論安全互動與成人陪同。"
        )
    else:
        tasks.append(
            "家庭共識：再次確認各人的照護分工，尤其是主要照顧者不在時，"
            "協助者是否真的願意接手。"
        )

    # 7. 期待與責任
    if data["飼養期待"] != "已安排／已確認":
        tasks.append(
            "飼養期待：討論毛孩的適應時間，以及掉毛、清潔、噪音、"
            "物品損耗或個性與期待不同時，可以如何求助和調整。"
        )

    # 8. 個體需求
    if data["個體需求"] != "已安排／已確認":
        tasks.append(
            "個體需求：向領養單位或原照顧者了解年齡、生活習慣、"
            "已知需求及適應情況，整理需要專業人員協助確認的事項。"
        )

    # 9. 備援
    if data["備援照顧者"] != "已安排／已確認":
        tasks.append(
            "緊急備援：詢問可信任的人是否願意在住院、出差或其他變故時協助；"
            "取得對方同意後，再討論照護內容。"
        )
    else:
        tasks.append(
            "緊急備援：再次確認協助者的意願、可協助時段與交接方式，"
            "不預設對方永遠有空。"
        )

    tasks.append(
        "短期不在家的備案：先找可信任的人協助；若無人可協助，"
        "可考慮寵物住宿，並事前確認業者資訊、環境、健康需求與緊急就醫安排。"
    )

    tasks.append(
        "長期安排：思考天災撤離、主要照顧者長期無法照護時的可能安排，"
        "並準備可更新的照護交接資訊。"
    )

    return tasks


def preparation_questions(data):
    questions = [
        "平日、假日與突發加班時，誰負責各項照護？",
        "日常與緊急支出目前有哪些安排，哪些仍待確認？",
        "若毛孩需要時間適應，家人或同住者能如何配合？",
        "領養單位或原照顧者知道哪些個體需求與生活習慣？",
        "住院、搬家或撤離時，誰願意協助？",
    ]

    if data["住處規定"] != "已確認允許":
        questions.insert(
            0,
            "租約、房東及管理規約是否允許飼養？能否確認相關約定？",
        )

    if data["居住檢查項目"] or data["動物"] in ["貓", "還沒決定"]:
        questions.append("窗戶、陽台、紗窗及固定方式是否需要專業人員評估？")

    if data["經濟準備"] == "目前不允許飼養":
        questions.append("若要調整條件，目前最需要先改善的是哪一項？")

    return questions


# ==================================================
# 現任飼主：困難情境
# ==================================================

SITUATIONS = {
    "搬家或租屋變動": [
        "確認新住處、租約、房東與管理規約是否允許飼養。",
        "檢查新住處門窗、陽台及其他可能逃脫的開口。",
        "若新住處尚未確定或無法立即入住，可考慮寵物住宿作為過渡方案。",
        "安排搬家當天的安全運輸、暫時照護與用品交接。",
        "向協助者說明毛孩的日常作息與適應需求。",
    ],
    "工作變忙、出差或旅行": [
        "列出不在家期間需要照護的時段與工作。",
        "詢問可信任的人是否願意協助，並確認日期及內容。",
        "若無人可協助，可考慮寵物住宿（寄宿）：事前確認業者的合法登記資訊、環境衛生、疫苗或健康證明需求、緊急就醫安排與收費方式。",
        "建議先安排短天數試住或實地參觀，觀察毛孩的適應情形，並提供熟悉的物品與作息資訊。",
        "整理日常用品、作息與必要交接資訊。",
    ],
    "飼主生病、受傷或住院": [
        "聯絡已同意協助的備援照顧者；如尚未安排，先詢問可信任的人。",
        "確認對方可協助的時間、地點與照護內容。",
        "整理毛孩作息、用品及需要交接的事項。",
        "若有特殊照護或用藥交接需求，請與獸醫師確認。",
    ],
    "經濟壓力或收入減少": [
        "盤點日常照護、必要就醫及其他近期支出。",
        "整理目前最急迫、需要討論的支出與時間。",
        "向可信任的人或相關單位詢問可能的支持，並自行查證資格與可用性。",
        "需要調整飲食或照護方式時，請先諮詢合格獸醫師。",
    ],
    "貓狗有逃脫或跳窗風險": [
        "找出最近發生或最可能發生的位置，例如窗戶、陽台、大門或縫隙。",
        "改善前，暫時限制接觸高風險開口，並安排有人陪同。",
        "確認晶片與寵物登記資料是否正確、聯絡方式是否最新。",
        "若已發生走失，請改依「毛孩走失」的步驟處理。",
    ],
    "毛孩行為讓我困擾": [
        "先記錄行為發生的時間、地點、頻率及當時情況，不急著推測原因。",
        "整理近期是否有環境、家庭成員或生活作息變動。",
        "記錄現有環境安排，以及其他讓你擔心的變化。",
        "若行為突然改變、持續發生或伴隨其他異常，請諮詢獸醫師。",
        "也可尋找具適當專業背景的人員討論；避免使用可能造成恐懼或傷害的處置。",
    ],
    "家人或同住者反對": [
        "整理對方具體擔心的事項，例如清潔、噪音、過敏或照護分工。",
        "討論哪些照護工作可以調整，以及每個人實際願意協助的程度。",
        "需要時請可信任的人協助溝通；不要預設家人一定能接手。",
    ],
    "家庭成員變化（懷孕、育兒或新同住者）": [
        "列出新成員到來後，可能增加或改變的照護工作與時間。",
        "與同住者討論新的照護分工，並確認寵物與新成員的互動安全。",
        "寵物與嬰幼兒之間的互動，應由成人全程看顧。",
        "若有過敏或不適，請諮詢醫師或獸醫師。",
    ],
    "同住關係改變（分居、離婚或同住者搬離）": [
        "先確認寵物的實際照護者與主要生活地點，避免在情緒激動時做決定。",
        "整理寵物的日常照護資訊、用品與就醫紀錄，方便雙方交接。",
        "若涉及寵物歸屬或費用分擔，可尋求適合的法律或調解資源協助。",
    ],
    "照顧壓力太大或感到孤立": [
        "先選出目前最困難的一項照護工作，不必一次解決所有問題。",
        "與可信任的人討論能否在特定時段分擔照護。",
        "整理簡短作息與照護資訊，降低交接負擔。",
        "若壓力已影響自身生活或安全，也可尋求適合的專業支持。",
    ],
    "毛孩年齡或照護需求改變": [
        "整理目前作息、日常照護及近期觀察到的變化。",
        "列出希望與獸醫師討論的問題，不自行推測原因或調整治療。",
        "和照顧者討論新的照護分工、時間與備援安排。",
    ],
    "災害或臨時撤離": [
        "以人與動物的安全為優先，遵循所在地官方發布的指示。",
        "在安全可行時，準備適合的運輸用品及必要照護資料。",
        "提前確認可攜帶動物的暫時安置安排，但實際可用性需再查證。",
        "與備援照顧者討論失聯或無法返家時的安排。",
    ],
    "毛孩走失": [
        "在確保自身安全的前提下，儘快聯絡所在地主管機關或相關單位詢問協尋方式。",
        "整理毛孩近期照片、外觀特徵及最後出現的時間與地點。",
        "確認寵物登記資料與聯絡方式是否正確。",
        "分享協尋資訊前，確認公開內容與個人隱私。",
    ],
    "其他困難或不知道怎麼辦": [
        "先寫下目前最需要協助的一件事，以及是否有急迫的安全需求。",
        "詢問可信任的人是否能提供短期支持。",
        "若暫時無法親自照護，先確認可行且安全的短期照顧安排。",
        "依問題性質，向獸醫師、主管機關或其他適合的專業人員諮詢。",
    ],
}

BEHAVIOR_DETAILS = {
    "無，目前沒有行為困擾": (
        "目前沒有行為困擾，可以維持現有的作息與照護方式；"
        "若之後出現行為改變，再回來記錄觀察內容。"
    ),
    "抓家具": (
        "可記錄抓家具發生的位置、時間與當時情況，"
        "以及家中是否有適合的抓握設施和擺放位置；將觀察結果帶去與專業人員討論。"
    ),
    "咬壞物品": (
        "記錄被咬的物品、發生時間及當時情況；先妥善收納可能造成危險的物品。"
    ),
    "吠叫或持續叫聲": (
        "記錄叫聲出現的時間、地點、持續情況及附近發生的事情，作為專業諮詢資訊。"
    ),
    "亂尿或排泄困擾": (
        "記錄發生時間、地點及其他變化；如有健康疑慮或情況突然改變，請儘快諮詢獸醫師。"
    ),
    "與人或其他動物互動衝突": (
        "優先避免人或動物受傷；記錄衝突發生前後的情況，"
        "並尋求獸醫師或適當專業人員協助。"
    ),
    "其他行為": (
        "記錄行為的時間、地點、頻率及前後情況，並整理希望向專業人員詢問的問題。"
    ),
}


def difficulty_tasks(data):
    tasks = list(SITUATIONS[data["困難類型"]])

    if (
        data["困難類型"] == "毛孩行為讓我困擾"
        and data["行為情境"] != "無，目前沒有行為困擾"
    ):
        tasks.insert(0, BEHAVIOR_DETAILS[data["行為情境"]])

    if data["備援照顧者"] != "已安排／已確認":
        tasks.append(
            "盤點可能協助照護的人，確認對方是否願意、何時可協助，以及能分擔哪些工作。"
        )

    return tasks


def difficulty_questions(data):
    questions = [
        "目前最急迫的事情是什麼？",
        "接下來幾天，誰願意協助、可以協助哪些部分？",
        "毛孩目前有哪些日常照護不能中斷？",
        "哪些問題需要詢問獸醫師或其他適合的專業人員？",
        "如果短期安排不可行，下一個可以確認的選項是什麼？",
    ]

    if data["困難類型"] == "毛孩行為讓我困擾":
        questions.extend([
            "行為從何時開始？通常在什麼時間、地點或情況下發生？",
            "近期環境、家庭成員或作息是否有變動？",
            "是否還有其他讓你擔心的變化？",
        ])

    return questions


# ==================================================
# 組合可編輯結果
# ==================================================

def build_preparation_report(data, tasks, questions):
    lines = [
        "執爪之約｜飼養前準備與承諾計畫",
        "這份內容是行動草案，不是飼養資格評分。",
        "",
        "【我的情況】",
    ]

    for key, value in data.items():
        lines.append(f"- {key}：{format_value(value)}")

    add_section(lines, "飼養前行動清單", tasks)
    add_section(lines, "可與家人或領養單位討論", questions)

    add_section(
        lines,
        "變故應對方案：可自行修改",
        [f"{change}：{CHANGE_PLANS[change]}" for change in data["可能變動"]]
        or ["尚未勾選可能的生活變動；建議重新檢視未來一至三年的計畫。"],
    )

    add_section(lines, "我的飼養承諾計畫：可自行修改", [
        f"主要照顧與分工：{safe_text(data['照護分工想法'])}",
        f"平日與特殊時段的照護：{safe_text(data['照護時間想法'])}",
        f"居住與環境安全：{safe_text(data['居住安全想法'])}",
        f"日常與緊急支出安排：{safe_text(data['經濟想法'])}",
        f"備援照顧安排：{safe_text(data['備援想法'])}",
        f"希望了解的個體需求：{safe_text(data['個體需求想法'])}",
        "回顧時間：建議每半年或生活變動時重新檢視一次。",
        "完成狀態：請自行標記已確認、進行中或待確認。",
    ])

    add_section(lines, "終養承諾句：可自行修改", [
        "我願意在生活條件改變時，先尋求支持、規劃備案，"
        "而不是在沒有評估前就直接放棄毛孩。",
    ])

    add_section(lines, "可修改的討論摘要", [
        f"我想了解飼養{data['動物']}前需要做的準備。",
        "目前希望與家人、同住者或領養單位討論照護分工、"
        "生活環境、個體需求及備援安排。",
        "尚待確認的事項請依實際情況修改後再分享。",
    ])

    lines.extend(["", "【重要提醒】", DISCLAIMER])
    return "\n".join(lines)


def build_difficulty_report(data, tasks, questions):
    lines = [
        "執爪之約｜困難應對與照護交接計畫",
        "遇到困難不代表你不在乎毛孩，我們先整理下一步。",
        "",
        "【我的情況】",
    ]

    for key, value in data.items():
        lines.append(f"- {key}：{format_value(value)}")

    add_section(lines, "現在可以做的事", tasks)
    add_section(lines, "待確認與專業諮詢問題", questions)
    add_section(lines, "棄養前最後防線：請依序評估", FINAL_STEPS)

    add_section(lines, "可修改的求助摘要", [
        f"目前主要困難：{data['困難類型']}。",
        f"毛孩類型：{data['動物']}。",
        f"具體情況：{safe_text(data['情況描述'])}。",
        f"希望獲得的協助：{safe_text(data['希望的協助'])}。",
        "分享前請確認內容，並自行刪除不想公開的資訊。",
    ])

    add_section(lines, "照護交接卡：可自行修改", [
        f"日常作息與照護：{safe_text(data['日常照護資訊'])}",
        f"特殊需求或須詢問獸醫師的事項：{safe_text(data['特殊需求'])}",
        f"協助者安排：{safe_text(data['備援想法'])}",
        "獸醫院及緊急聯絡資訊：待使用者自行確認後補入。",
        "真實姓名、電話、地址與病歷：建議下載後再於本機補入。",
    ])

    lines.extend(["", "【重要提醒】", DISCLAIMER])
    return "\n".join(lines)


# ==================================================
# AI：使用者同意後才傳送
# ==================================================

def create_ai_plan(mode, data, tasks):
    from openai import OpenAI

    client = OpenAI()

    message = (
        f"使用情境：{mode}\n"
        f"使用者提供的資料：{data}\n"
        f"規則式待辦事項：{tasks}\n\n"
        "請依照指示整理成可供使用者確認與修改的行動草案。"
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=AI_INSTRUCTIONS,
        input=message,
    )

    return response.output_text


# ==================================================
# 網站首頁
# ==================================================

st.title("🐾 執爪之約")
st.caption(f"{ENGLISH_NAME}｜讓每一份陪伴，都有準備。")

st.write(
    "每位飼主都有自己的生活節奏與限制，每隻毛孩都需要穩定的照顧。"
    "從飼養前準備、責任教育，到生活出現變化時的支持，"
    "一起把承諾拆成可以執行的下一步。"
)

st.info(
    "這是開發中的原型：不評分、不判定你是否有資格飼養，"
    "也不替你做領養、安置或轉送的決定。"
)

st.warning(PRIVACY_NOTICE)

mode = st.radio(
    "選擇你目前需要的協助：",
    [
        "我想養貓或狗",
        "我現在遇到困難，需要幫忙",
    ],
    horizontal=True,
)

form_tab, education_tab = st.tabs([
    "📝 開始整理我的計畫",
    "📚 情境教育與責任認識",
])


# ==================================================
# 情境教育
# ==================================================

with education_tab:
    st.header("責任教育：先想一想，不是考試")

    st.write(
        "每個家庭與每隻貓狗都不一樣。"
        "以下情境是幫助你和家人討論，不會計分。"
    )

    with st.expander("🚪 貓咪沒有紗窗，窗邊很危險"):
        st.write(
            "有紗窗也不代表一定安全，紗窗可能被撐開或扯落。"
            "可先檢查窗戶與陽台的固定方式，改善前避免貓咪單獨接觸開窗。"
            "若曾經發生跑出去的情況，請確認晶片與登記資料是否正確。"
        )

    with st.expander("💰 想養，但經濟現在還不允許"):
        st.write(
            "愛與責任之外，日常飲食、定期照護與緊急醫療都需要長期支出。"
            "若目前條件還不允許，可以先暫緩接回毛孩，"
            "把需要達成的條件寫成清單，逐步準備。"
        )

    with st.expander("🛋️ 寵物破壞家具，家人很累"):
        st.write(
            "先記錄破壞發生的時間、地點與當時情況，"
            "再整理環境與作息是否有可以調整的地方。"
            "若行為持續或伴隨其他異常，請諮詢獸醫師或適當專業人員。"
        )

    with st.expander("🐱 貓咪剛到家一直躲起來"):
        st.write(
            "新環境可能需要適應時間，不要急著推斷原因或強迫互動。"
            "可先確認環境安排，並向原照顧者、領養單位或獸醫師"
            "詢問個體需求。若有健康疑慮，請諮詢獸醫師。"
        )

    with st.expander("🐶 狗狗外出時可能掙脫裝備"):
        st.write(
            "事先確認外出裝備是否適合個體、狀況是否良好，"
            "以及出入口安全。沒有任何裝備能保證絕對不會逃脫。"
        )

    with st.expander("🏠 房東口頭說可以養，租約卻沒寫"):
        st.write(
            "可以再次確認租約、房東及管理規約的相關條件，"
            "並詢問能否明確記錄約定。搬家前也應確認新住處規定。"
        )

    with st.expander("⏰ 未來工作變忙，誰來照顧？"):
        st.write(
            "先列出日常照護工作，再和可能協助的人確認意願、"
            "時間與分工。家人住得近，不代表已經同意或隨時有空。"
        )

    with st.expander("🤝 如果真的無法繼續照顧"):
        st.write(
            "可以先盤點短期支持與備援；若仍無法繼續照顧，"
            "向主管機關或可信任的動保相關單位諮詢妥善安置與交接。"
            "這不是對你的責備，而是一起避免照護中斷。"
        )

    st.warning(DISCLAIMER)


# ==================================================
# 兩個表單入口
# ==================================================

with form_tab:
    if mode == "我想養貓或狗":
        st.header("🏠 飼養前準備")

        st.write(
            "以下問題涵蓋八個面向。請依目前情況回答；"
            "不知道或尚未安排，都可以選擇「待確認」。"
        )

        with st.form("preparation_form"):
            st.subheader("1. 動物與日常照護")

            pet = st.selectbox(
                "想飼養的動物",
                ["貓", "狗", "還沒決定"],
            )

            daily = yes_no_pending(
                "日常照護時間與分工是否已有安排？",
                "p_daily",
            )

            care_split = st.text_input(
                "主要照護與分工想法（選填；不填姓名）",
                placeholder="例如：我負責平日照護，假日分工待討論",
            )

            care_time = st.text_input(
                "平日或特殊時段的照護想法（選填）",
                placeholder="例如：白天上班，加班時需要備援",
            )

            absence = st.selectbox(
                "平均每週有多少時間會不在家（含出差、加班）？",
                [
                    "很少，每週不到 1 天",
                    "每週 1–2 天",
                    "每週 3 天以上",
                    "經常出差或長時間外出",
                    "待確認",
                ],
                key="p_absence",
            )

            backup_plans = st.multiselect(
                "短期不在家時，可能的備案（可多選）",
                [
                    "可信任的親友協助",
                    "寵物住宿（寄宿）",
                    "居家或到府照護服務",
                    "暫時寄養",
                    "尚未規劃",
                ],
                key="p_backup_plans",
            )

            st.subheader("2. 經濟與支出")

            budget = st.selectbox(
                "目前經濟狀況是否能支持日常與緊急照護？",
                MONEY_STATUS,
                key="p_budget",
            )

            budget_note = st.text_input(
                "經濟準備想法（選填；不填精確收入）",
                placeholder="例如：需要再盤點日常與緊急支出",
            )

            st.subheader("3. 居住環境與逃脫風險")

            safety_items = st.multiselect(
                "住處目前有哪些需要檢查或改善的情況？（可多選；沒有可不選）",
                list(HOME_SAFETY_CHECKS.keys()),
                key="p_safety",
            )

            chip = st.selectbox(
                "寵物晶片與登記資料狀態",
                CHIP_STATUS,
                key="p_chip",
            )

            home_note = st.text_input(
                "居住安全想法（選填）",
                placeholder="例如：客廳窗戶的紗窗待確認",
            )

            st.subheader("4. 租屋與搬遷")

            housing = st.selectbox(
                "住處、租約及相關規定是否允許飼養？",
                ["尚未確認", "已確認允許", "目前不允許"],
            )

            moving = yes_no_pending(
                "搬家或租約到期時的居住備案是否已有安排？",
                "p_moving",
            )

            st.subheader("5. 家庭與照護共識")

            family_view = st.selectbox(
                "家人或同住者的意見",
                FAMILY_VIEWS,
                key="p_family_view",
            )

            st.subheader("6. 飼養期待與責任")

            expectations = yes_no_pending(
                "是否已討論適應期、清潔、噪音及意外狀況？",
                "p_expectations",
            )

            st.subheader("7. 毛孩個體需求")

            individual = yes_no_pending(
                "是否已了解或規劃詢問毛孩的個體需求？",
                "p_individual",
            )

            individual_note = st.text_input(
                "希望了解的個體需求（選填；不填真實病歷）",
                placeholder="例如：生活習慣、活動需求及適應情況",
            )

            st.subheader("8. 緊急備援與長期安排")

            backup = yes_no_pending(
                "是否已有事先同意的備援照顧者？",
                "p_backup",
            )

            backup_note = st.text_input(
                "備援或長期安排想法（選填；不填姓名與電話）",
                placeholder="例如：尚未詢問親友是否願意協助",
            )

            st.subheader("9. 生活變動與變故應對")

            life_changes = st.multiselect(
                "未來一至三年，哪些生活變動可能發生？（可多選）",
                list(CHANGE_PLANS.keys()),
                key="p_changes",
            )

            prep_submit = st.form_submit_button(
                "產生準備清單與承諾計畫",
                type="primary",
            )

        if prep_submit:
            data = {
                "動物": pet,
                "日常照護": daily,
                "經濟準備": budget,
                "居住檢查項目": safety_items,
                "晶片與登記": chip,
                "住處規定": housing,
                "搬遷備案": moving,
                "家人意見": family_view,
                "飼養期待": expectations,
                "個體需求": individual,
                "備援照顧者": backup,
                "不在家情形": absence,
                "短期備案": backup_plans,
                "可能變動": life_changes,
                "照護分工想法": care_split,
                "照護時間想法": care_time,
                "經濟想法": budget_note,
                "居住安全想法": home_note,
                "個體需求想法": individual_note,
                "備援想法": backup_note,
            }

            tasks = preparation_tasks(data)
            questions = preparation_questions(data)
            report = build_preparation_report(data, tasks, questions)

            version = st.session_state.get("result_version", 0) + 1
            st.session_state["result_version"] = version
            st.session_state["result"] = {
                "version": version,
                "mode": mode,
                "data": data,
                "tasks": tasks,
                "report": report,
            }

    else:
        st.header("🤝 遇到困難，我們一起整理")

        st.write(
            "生活可能發生變化。先選擇目前最需要協助的情況，"
            "再整理安全、照護與求助的下一步。"
        )

        with st.form("difficulty_form"):
            pet = st.selectbox(
                "你的毛孩是？",
                ["貓", "狗"],
            )

            situation = st.selectbox(
                "目前最需要協助的情況",
                list(SITUATIONS.keys()),
            )

            behavior = st.selectbox(
                "如果有行為困擾，最接近哪一種？（其他情況可保留預設）",
                list(BEHAVIOR_DETAILS.keys()),
            )

            backup = yes_no_pending(
                "是否已有事先同意的備援照顧者？",
                "d_backup",
            )

            situation_note = st.text_area(
                "簡單描述情況（選填）",
                placeholder=(
                    "例如：貓咪抓沙發，家人感到困擾；"
                    "不要輸入姓名、地址、電話或真實病歷。"
                ),
                max_chars=500,
            )

            help_note = st.text_input(
                "希望獲得什麼協助？（選填）",
                placeholder="例如：整理諮詢問題、尋找短期照顧安排",
            )

            daily_note = st.text_area(
                "交接卡：日常作息與照護（選填）",
                placeholder="例如：早晚需要照護，詳細時間待確認",
                max_chars=500,
            )

            special_note = st.text_area(
                "交接卡：特殊需求或想詢問獸醫師的事項（選填）",
                placeholder="請使用不具識別性的描述，不填真實病歷",
                max_chars=500,
            )

            backup_note = st.text_input(
                "交接卡：備援安排想法（選填）",
                placeholder="例如：需要先詢問親友是否願意協助",
            )

            difficulty_submit = st.form_submit_button(
                "產生應對清單、求助摘要與交接卡",
                type="primary",
            )

        if difficulty_submit:
            data = {
                "動物": pet,
                "困難類型": situation,
                "備援照顧者": backup,
                "情況描述": situation_note,
                "希望的協助": help_note,
                "日常照護資訊": daily_note,
                "特殊需求": special_note,
                "備援想法": backup_note,
            }

            if situation == "毛孩行為讓我困擾":
                data["行為情境"] = behavior

            tasks = difficulty_tasks(data)
            questions = difficulty_questions(data)
            report = build_difficulty_report(data, tasks, questions)

            version = st.session_state.get("result_version", 0) + 1
            st.session_state["result_version"] = version
            st.session_state["result"] = {
                "version": version,
                "mode": mode,
                "data": data,
                "tasks": tasks,
                "report": report,
            }

    # ==================================================
    # 結果：可編輯、可下載
    # ==================================================

    result = st.session_state.get("result")

    if result and result["mode"] == mode:
        st.divider()
        st.header("📋 你的行動計畫")

        st.write(
            "以下內容是依照你的選擇整理的草案。"
            "你可以直接修改文字，再決定是否下載或分享。"
        )

        st.warning(DISCLAIMER)

        report_key = f"report_edit_{result['version']}"

        edited_report = st.text_area(
            "編輯行動清單、摘要與交接內容",
            value=result["report"],
            height=480,
            key=report_key,
        )

        st.warning(DISCLAIMER)

        st.download_button(
            label="📥 下載我編輯後的行動計畫",
            data=edited_report.encode("utf-8-sig"),
            file_name="執爪之約_行動計畫.txt",
            mime="text/plain",
        )

        st.caption(
            "請自行確認內容後再分享。下載的文字檔可在你的電腦上繼續編輯。"
        )

        # ==================================================
        # 選用 AI
        # ==================================================

        st.divider()
        st.header("✨ 選用：AI 整理草案")

        st.write(
            "AI 可根據你在表單中填寫的內容與程式產生的待辦事項，"
            "整理下一步和求助摘要。它使用的是表單資料與原始待辦，"
            "不是上方編輯框中後來修改的文字。"
        )

        st.caption(
            "使用 AI 會將表單資料及待辦事項傳送給 OpenAI，"
            "並可能產生 API 費用。請先確認第三方服務的資料處理條件；"
            "不要輸入可識別資料。AI 內容可能有錯，需自行確認。"
        )

        api_key_available = bool(os.getenv("OPENAI_API_KEY"))

        if not api_key_available:
            st.info(
                "目前沒有偵測到 OPENAI_API_KEY。"
                "上方規則式清單、編輯與下載功能仍可正常使用。"
            )
        else:
            consent_key = f"ai_consent_{result['version']}"

            consent = st.checkbox(
                "我了解並同意將本次表單內容與待辦事項傳送至 OpenAI 進行整理。",
                key=consent_key,
            )

            if st.button(
                "使用 AI 整理",
                disabled=not consent,
                key=f"ai_button_{result['version']}",
            ):
                try:
                    with st.spinner("正在整理，請稍候……"):
                        ai_output = create_ai_plan(
                            result["mode"],
                            result["data"],
                            result["tasks"],
                        )

                    st.session_state[
                        f"ai_output_{result['version']}"
                    ] = ai_output

                except Exception:
                    st.error(
                        "AI 整理暫時無法使用。請檢查 API 金鑰、"
                        "帳戶與模型使用權限、額度或網路連線。"
                        "基本清單仍可使用；不要公開貼上金鑰。"
                    )

        ai_output = st.session_state.get(
            f"ai_output_{result['version']}",
            "",
        )

        if ai_output:
            st.subheader("AI 草案：請先檢查與修改")

            edited_ai = st.text_area(
                "編輯 AI 草案",
                value=ai_output,
                height=300,
                key=f"ai_edit_{result['version']}",
            )

            st.warning(
                "AI 可能產生錯誤或不完整內容，也可能不遵守指示。"
                "請自行檢查；健康與行為問題請諮詢適當專業人員。"
            )

            st.warning(DISCLAIMER)

            st.download_button(
                label="📥 下載我編輯後的 AI 草案",
                data=edited_ai.encode("utf-8-sig"),
                file_name="執爪之約_AI草案.txt",
                mime="text/plain",
            )

st.divider()
st.caption(
    "執爪之約｜協助整理照護計畫與支持選項，"
    "不保證能避免照護中斷或棄養。"
)
