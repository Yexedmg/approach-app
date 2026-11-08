"""
The full math behind approaching — 5 layers of truth.

1. Per-encounter expected value (what one hello is actually worth)
2. Compounding skill (you get better with practice, and it multiplies everything)
3. Regret modeling (the irreversible cost of silence, day by day)
4. Conversation funnel (hello → real convo → number → date → relationship)
5. Time decay (each remaining day is worth more than the last)
"""

import math

# ============================================================
# YOUR NUMBERS — adjust these to match your reality
# ============================================================
PEOPLE_PER_DAY = 10          # eligible people you see daily
TOTAL_DAYS = int(6.5 * 30)   # ~195 days left in window
APPROACHES_PER_DAY = 3        # how many you'll actually talk to

# Re-encounter probabilities
CHANCE_SEE_AGAIN = 0.10       # 10% chance you see her a 2nd time
CHANCE_SEE_THIRD = 0.05       # 5% chance after 2nd time

# Funnel conversion rates (baseline, before skill boost)
HELLO_TO_CONVO = 0.40         # 40% of hellos become real conversations
CONVO_TO_NUMBER = 0.30        # 30% of real convos lead to getting a number
NUMBER_TO_DATE = 0.40         # 40% of numbers become actual dates
DATE_TO_RELATIONSHIP = 0.10   # 10% of dates lead to a relationship


# ============================================================
# 2. COMPOUNDING SKILL MODEL
# ============================================================
def skill_multiplier(total_conversations):
    """
    Every conversation makes you better. Logarithmic curve:
    fast gains early (rewarding you for starting), diminishing later.

      0 convos → 1.00x (baseline, you're new)
     10 convos → 1.52x
     50 convos → 1.84x
    100 convos → 1.99x
    200 convos → 2.14x
    500 convos → 2.34x

    This multiplier applies to ALL funnel rates.
    """
    return 1 + 0.15 * math.log2(1 + total_conversations)


def boosted_rate(base_rate, skill_mult):
    """Apply skill boost to a conversion rate, capped at 90% (nothing is certain)."""
    return min(0.90, base_rate * skill_mult)


# ============================================================
# 5. TIME DECAY MODEL
# ============================================================
def urgency_multiplier(days_left, total_days):
    """
    As the window shrinks, each remaining day is worth more.
    The total opportunity stays the same — it's just compressed into fewer days.

    Day   1/195 → 1.0x
    Day  50/195 → 1.34x
    Day 100/195 → 2.05x
    Day 150/195 → 4.33x
    Day 180/195 → 13.0x
    Day 190/195 → 39.0x

    Translation: waiting makes every remaining day carry exponentially more weight.
    """
    if days_left <= 0:
        return float('inf')
    return total_days / days_left


# ============================================================
# MAIN SIMULATION
# ============================================================
def run():
    total_unique = PEOPLE_PER_DAY * TOTAL_DAYS
    total_conversations = APPROACHES_PER_DAY * TOTAL_DAYS
    total_silent = total_unique - total_conversations

    print("=" * 60)
    print("  THE MATH OF APPROACHING — YOUR REALITY IN NUMBERS")
    print("=" * 60)
    print(f"\n  Window: {TOTAL_DAYS} days | {PEOPLE_PER_DAY} people/day | {APPROACHES_PER_DAY} talks/day")
    print(f"  Total people you'll see: {total_unique:,}")
    print(f"  Total you'll talk to: {total_conversations:,}")
    print(f"  Total you'll ignore: {total_silent:,}")

    # ===========================================================
    # 1. PER-ENCOUNTER EXPECTED VALUE
    # ===========================================================
    print(f"\n{'─' * 60}")
    print("  1. WHAT ONE HELLO IS WORTH")
    print(f"{'─' * 60}")

    vanish_rate = 1 - CHANCE_SEE_AGAIN  # 90%
    print(f"\n  If you DON'T speak:")
    print(f"    → {vanish_rate:.0%} chance she disappears from your life forever")
    print(f"    → {CHANCE_SEE_AGAIN:.0%} chance you see her once more")
    print(f"    → {CHANCE_SEE_AGAIN * CHANCE_SEE_THIRD:.1%} chance you see her a 3rd time")
    print(f"    → Expected connections: 0")

    print(f"\n  If you DO speak:")
    print(f"    → {HELLO_TO_CONVO:.0%} chance it becomes a real conversation")
    print(f"    → {HELLO_TO_CONVO * CONVO_TO_NUMBER:.0%} chance you get her number")
    print(f"    → {HELLO_TO_CONVO * CONVO_TO_NUMBER * NUMBER_TO_DATE:.1%} chance of a date")
    print(f"    → Cost: 5 seconds + mild discomfort")

    print(f"\n  ★ One hello: {HELLO_TO_CONVO:.0%} chance of something real")
    print(f"  ★ Silence:   0% chance of anything")
    print(f"  ★ The math ALWAYS favors speaking")

    # ===========================================================
    # 2. COMPOUNDING SKILL
    # ===========================================================
    print(f"\n{'─' * 60}")
    print("  2. COMPOUNDING SKILL (you get better every time)")
    print(f"{'─' * 60}")

    milestones = [0, 10, 25, 50, 100, 200, total_conversations]
    print(f"\n  {'Conversations':>15}  {'Skill Mult':>12}  {'Hello→Convo':>12}  {'Hello→Number':>13}")
    for m in milestones:
        sm = skill_multiplier(m)
        eff_convo = boosted_rate(HELLO_TO_CONVO, sm)
        eff_number = eff_convo * boosted_rate(CONVO_TO_NUMBER, sm)
        label = f"{m}" if m != total_conversations else f"{m} (you)"
        print(f"  {label:>15}  {sm:>11.2f}x  {eff_convo:>11.0%}  {eff_number:>12.0%}")

    final_skill = skill_multiplier(total_conversations)
    print(f"\n  After {total_conversations} conversations, your skill multiplier: {final_skill:.2f}x")
    print(f"  Your hello→convo rate goes from {HELLO_TO_CONVO:.0%} → {boosted_rate(HELLO_TO_CONVO, final_skill):.0%}")
    print(f"  Every funnel stage improves. Early conversations have outsized value")
    print(f"  because they unlock better rates for all future ones.")

    # ===========================================================
    # 4. CONVERSATION FUNNEL (with progressive skill)
    # ===========================================================
    print(f"\n{'─' * 60}")
    print("  4. YOUR CONVERSATION FUNNEL")
    print(f"{'─' * 60}")

    # Simulate day by day with skill building
    running_total = 0
    total_convos = 0
    total_numbers = 0
    total_dates = 0
    total_relationships = 0

    for day in range(TOTAL_DAYS):
        sm = skill_multiplier(running_total)
        for _ in range(APPROACHES_PER_DAY):
            running_total += 1
            r_convo = boosted_rate(HELLO_TO_CONVO, sm)
            r_number = boosted_rate(CONVO_TO_NUMBER, sm)
            r_date = boosted_rate(NUMBER_TO_DATE, sm)
            r_rel = boosted_rate(DATE_TO_RELATIONSHIP, sm)

            total_convos += r_convo
            total_numbers += r_convo * r_number
            total_dates += r_convo * r_number * r_date
            total_relationships += r_convo * r_number * r_date * r_rel

    second_meetings = total_conversations * CHANCE_SEE_AGAIN
    third_meetings = second_meetings * CHANCE_SEE_THIRD

    bar_max = total_conversations
    stages = [
        ("Hellos", total_conversations, total_conversations),
        ("Real convos", total_convos, total_conversations),
        ("Numbers", total_numbers, total_conversations),
        ("2nd meetings", second_meetings, total_conversations),
        ("Dates", total_dates, total_conversations),
        ("Relationships", total_relationships, total_conversations),
    ]

    print()
    for name, count, base in stages:
        pct = count / base * 100 if base > 0 else 0
        bar_len = int(pct / 100 * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"  {name:<14} {bar} {count:>7.1f}  ({pct:.1f}%)")

    print(f"\n  From {total_conversations} hellos over {TOTAL_DAYS} days:")
    print(f"    → {total_convos:.0f} real conversations")
    print(f"    → {total_numbers:.0f} phone numbers")
    print(f"    → {second_meetings:.0f} second meetings")
    print(f"    → {total_dates:.1f} dates")
    print(f"    → {total_relationships:.1f} relationships")

    # ===========================================================
    # 3. REGRET MODELING
    # ===========================================================
    print(f"\n{'─' * 60}")
    print("  3. IRREVERSIBLE LOSS (what silence costs)")
    print(f"{'─' * 60}")

    gone_forever = int(total_silent * vanish_rate)
    # What those people could have become (at baseline skill — you didn't earn the boost)
    lost_convos = total_silent * HELLO_TO_CONVO
    lost_numbers = lost_convos * CONVO_TO_NUMBER
    lost_dates = lost_numbers * NUMBER_TO_DATE
    lost_relationships = lost_dates * DATE_TO_RELATIONSHIP

    print(f"\n  People you'll see but never talk to: {total_silent:,}")
    print(f"  Of those, gone from your life permanently: {gone_forever:,}")
    print(f"\n  What was hiding in that silence:")
    print(f"    → {lost_convos:.0f} real conversations you'll never have")
    print(f"    → {lost_numbers:.0f} numbers you'll never get")
    print(f"    → {lost_dates:.0f} dates that will never happen")
    print(f"    → {lost_relationships:.1f} relationships that will never exist")
    print(f"\n  Every person you ignore is a door closing permanently.")
    print(f"  {vanish_rate:.0%} of them — gone. No second chance. No undo button.")

    # ===========================================================
    # 5. TIME DECAY
    # ===========================================================
    print(f"\n{'─' * 60}")
    print("  5. THE SHRINKING WINDOW (each day is worth more)")
    print(f"{'─' * 60}")

    checkpoints = [1, 30, 60, 100, 130, 160, 180, 190, 195]
    print(f"\n  {'Day':>6}  {'Days left':>10}  {'Urgency':>10}  {'What it means':>30}")
    for d in checkpoints:
        if d > TOTAL_DAYS:
            continue
        left = TOTAL_DAYS - d
        urg = urgency_multiplier(left, TOTAL_DAYS)
        if urg == float('inf'):
            urg_str = "∞"
            meaning = "Window closed"
        elif urg < 2:
            urg_str = f"{urg:.1f}x"
            meaning = "Comfortable, but ticking"
        elif urg < 5:
            urg_str = f"{urg:.1f}x"
            meaning = "Getting real"
        elif urg < 15:
            urg_str = f"{urg:.1f}x"
            meaning = "Every day matters now"
        else:
            urg_str = f"{urg:.1f}x"
            meaning = "NOW or never"
        print(f"  {d:>6}  {left:>10}  {urg_str:>10}  {meaning:>30}")

    print(f"\n  You are on day 1. The urgency is 1.0x.")
    print(f"  By day 180, it's 13x. Same opportunity, fraction of the time.")
    print(f"  Starting today means every future day benefits from your skill.")
    print(f"  Starting later means higher urgency AND lower skill.")

    # ===========================================================
    # FINAL VERDICT
    # ===========================================================
    print(f"\n{'=' * 60}")
    print("  THE BOTTOM LINE")
    print(f"{'=' * 60}")
    print(f"""
  You will see {total_unique:,} people in {TOTAL_DAYS} days.
  Talking to {APPROACHES_PER_DAY}/day gives you {total_conversations} conversations.
  Those {total_conversations} conversations become:
    {total_numbers:.0f} numbers, {total_dates:.1f} dates, {total_relationships:.1f} relationships.

  Staying silent means {gone_forever:,} people vanish forever,
  taking {lost_dates:.0f} potential dates with them.

  The cost of one hello: 5 seconds.
  The cost of silence: permanent.

  You will never be younger than right now. Neither will they.
  The window is open. It's closing. Speak.
""")


if __name__ == "__main__":
    run()
