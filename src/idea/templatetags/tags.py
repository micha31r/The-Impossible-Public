from django import template
import math

register = template.Library()

@register.filter(name="times")
def times(value):
	return range(value)

@register.filter(name="length")
def length(value):
	return len(value)

# Convert number to text e.g: 1100 -> 1.1k 
@register.filter(name="ntt")
def ntt(value):
	string = ""
	divided = math.floor(value / 1000)
	if divided >= 1 and divided < 10:
		string = f"{round(value/1000,1)}k"
	elif divided >= 10 and divided < 1000:
		string = f"{divided}k" 
	elif divided >= 1000 and divided < 10000:
		string = f"{round(divided/1000,1)}m" 
	elif divided >= 10000:
		string = "∞"
	else:
		string = value
	return string