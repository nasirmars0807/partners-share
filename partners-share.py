# 这个程序根据合同要求计算每个合伙人最后应该分得的钱。
# 运行程序可以翻墙后访问Google Colab网页：https://colab.research.google.com/ 新建文本粘贴所有程序即可。
# F会依照计划，每个月低更新一次，如果有转账需要及时更新。
# F不需要公开买入的公司，但是向合伙人需要公开账单以便查账。
# 状态：未启用
# 最后一次更新时间： 2025年7月21日
# 预计下一次更新时间： 2025年7月31日

from decimal import Decimal, ROUND_FLOOR

F_start = Decimal('10600.0')    # F先生的之前投入资金（最后更新时间：2025年7月20日）
L_start = Decimal('1000.0')        # L先生的之前投入资金（最后更新时间：2025年7月20日）
Z_start = Decimal('2000.0')        # Z先生的之前投入资金（最后更新时间：2025年7月20日）
total_end = Decimal('13600.0')  # 结算资金（投资后）（最后更新时间：未启用）

# Calculate total starting capital
total_start = F_start + L_start + Z_start
print(f"投入总资金: {total_start.quantize(Decimal('0.01'), ROUND_FLOOR)}")

if total_start <= 0:
    print("Total beginning capital must be positive.")
else:
    # Calculate gain percentage
    gain_pct = ((total_end - total_start) / total_start) * Decimal('100') if total_start > 0 else Decimal('0.0')
    print(f"月盈利百分比: {gain_pct.quantize(Decimal('0.01'), ROUND_FLOOR)}%")

    # Proportions
    proportions = {
        'F先生': F_start / total_start,
        'L先生': L_start / total_start,
        'Z先生': Z_start / total_start
    }
    print("\n投入资金每人比例:")
    for person, prop in proportions.items():
        prop_pct = (prop * Decimal('100')).quantize(Decimal('0.01'), ROUND_FLOOR)
        print(f"{person}: {prop_pct}%")

    # Total profit or loss
    profit = total_end - total_start
    print(f"\n当月总盈利/亏损（单位：美金）: {profit.quantize(Decimal('0.01'), ROUND_FLOOR)}$")

    finals = {}
    if profit <= 0:
        print("当月没有盈利，不需要抽成")
        finals['F先生'] = proportions['F先生'] * total_end
        finals['L先生'] = proportions['L先生'] * total_end
        finals['Z先生'] = proportions['Z先生'] * total_end
        print("\n详情:")
        print(f"F先生: 占比 {proportions['F先生'].quantize(Decimal('0.01'), ROUND_FLOOR)} * 当月结算总资金 {total_end.quantize(Decimal('0.01'), ROUND_FLOOR)}$ = {finals['F先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$")
        print(f"L先生: 占比 {proportions['L先生'].quantize(Decimal('0.01'), ROUND_FLOOR)} * 当月结算总资金 {total_end.quantize(Decimal('0.01'), ROUND_FLOOR)}$ = {finals['L先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$")
        print(f"Z先生: 占比 {proportions['Z先生'].quantize(Decimal('0.01'), ROUND_FLOOR)} * 当月结算总资金 {total_end.quantize(Decimal('0.01'), ROUND_FLOOR)}$ = {finals['Z先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$")
    else:
        # Determine fee rate
        if 0 < gain_pct < 25:
            fee_rate = Decimal('0.2')
        elif 25 <= gain_pct < 40:
            fee_rate = Decimal('0.3')
        elif 40 <= gain_pct:
            fee_rate = Decimal('0.4')
        else:
            fee_rate = Decimal('0')  # Should not happen if profit > 0

        print(f"当月有盈利，需要向F先生提供盈利部分的抽成比: {fee_rate * Decimal('100'):.0f}%")

        # Individual profits
        profits = {
            'F先生': proportions['F先生'] * profit,
            'L先生': proportions['L先生'] * profit,
            'Z先生': proportions['Z先生'] * profit
        }
        print("\n抽成前每人的盈亏资金:")
        for person, prof in profits.items():
            print(f"{person}: 占比 {proportions[person].quantize(Decimal('0.01'), ROUND_FLOOR)} x 总盈亏 {profit.quantize(Decimal('0.01'), ROUND_FLOOR)} = {prof.quantize(Decimal('0.01'), ROUND_FLOOR)}")

        # Fees
        fee_from_L = fee_rate * profits['L先生']
        fee_from_Z = fee_rate * profits['Z先生']
        print("\n向F先生提供的抽成:")
        print(f"L先生的盈利部分: {profits['L先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$ x 抽成{fee_rate * Decimal('100'):.0f}% = {fee_from_L.quantize(Decimal('0.01'), ROUND_FLOOR)}$")
        print(f"Z先生的盈利部分: {profits['L先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$ x 抽成{fee_rate * Decimal('100'):.0f}% = {fee_from_L.quantize(Decimal('0.01'), ROUND_FLOOR)}$")

        # Final amounts
        finals['F先生'] = F_start + profits['F先生'] + fee_from_L + fee_from_Z
        finals['L先生'] = L_start + profits['L先生'] - fee_from_L
        finals['Z先生'] = Z_start + profits['Z先生'] - fee_from_Z

        print("\n最后每人分成计算:")
        print(f"F先生: 投入资金 {F_start.quantize(Decimal('0.01'), ROUND_FLOOR)}$ + 当月盈亏 {profits['F先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$ + 获得L先生的抽成 {fee_from_L.quantize(Decimal('0.01'), ROUND_FLOOR)}$ + 获得Z先生的抽成 {fee_from_Z.quantize(Decimal('0.01'), ROUND_FLOOR)}$ = {finals['F先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$")
        print(f"L先生: 投入资金 {L_start.quantize(Decimal('0.01'), ROUND_FLOOR)}$ + 当月盈亏 {profits['L先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$ - 扣除的抽成 {fee_from_L.quantize(Decimal('0.01'), ROUND_FLOOR)} = {finals['L先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$")
        print(f"Z先生: 投入资金 {Z_start.quantize(Decimal('0.01'), ROUND_FLOOR)}$ + 当月盈亏 {profits['Z先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$ - 扣除的抽成 {fee_from_Z.quantize(Decimal('0.01'), ROUND_FLOOR)} = {finals['Z先生'].quantize(Decimal('0.01'), ROUND_FLOOR)}$")

    # Truncate and adjust to avoid exceeding and match total
    truncated = {person: finals[person].quantize(Decimal('0.01'), ROUND_FLOOR) for person in finals}
    sum_trunc = sum(truncated.values())
    diff = total_end - sum_trunc
    truncated['F先生'] += diff

    # Print the results
    print("\n月结后金额:")
    for person, amount in truncated.items():
        print(f"{person} 分得: {amount}$")

    # Check if the sum matches total_end
    total_final = sum(truncated.values())
    print(f"用于检验：计算后资金 {total_final} (真实剩余资金 {total_end}) 查验通过✅")
