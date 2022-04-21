from django import template

register = template.Library() 

@register.filter(name="laptop_upvoted")
def laptop_upvoted(laptop, user):
    vote = laptop.laptopvote_set.filter(user=user)
    if vote.exists():
        if vote[0].vote_type:
            return "upvoted"
    else:
        return ""

@register.filter(name="laptop_downvoted")
def laptop_downvoted(laptop, user):
    vote = laptop.laptopvote_set.filter(user=user)
    if vote.exists():
        if not vote[0].vote_type:
            return "downvoted"
    else:
        return ""

@register.filter(name="part_upvoted")
def part_upvoted(part, user):
    vote = part.partvote_set.filter(user=user)
    if vote.exists():
        if vote[0].vote_type:
            return "upvoted"
    else:
        return ""

@register.filter(name="part_downvoted")
def part_downvoted(part, user):
    vote = part.partvote_set.filter(user=user)
    if vote.exists():
        if not vote[0].vote_type:
            return "downvoted"
    else:
        return ""

@register.filter(name="verified")
def verified(laptop):
    if laptop.verified:
        return "fa fa-solid fa-circle-check icon verified"
    else:
        return ""