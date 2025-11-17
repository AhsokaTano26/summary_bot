import ast

input_str = "[1016925587,339834885,1017112832,962870444,825771260]"
output_list = ast.literal_eval(input_str)

print(input_str)
print(type(input_str))
print(output_list)
print(type(output_list))
# 输出: [1016925587, 339834885, 1017112832, 962870444, 825771260]
# 输出: <class 'list'>