import math

# اولویت عملگرها (عدد بزرگتر = اولویت بیشتر)
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3,
}

FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'arcsin': math.asin,
    'arccos': math.acos,
    'arctan': math.atan,
    'ln': math.log,       
    'log': math.log10,    
    'exp': math.exp,
    'sqrt': math.sqrt,
    'abs': math.fabs,
}

def is_number(token):

    try:
        float(token)
        return True
    except ValueError:
        return False


def infix_to_postfix(expression):
    
    
    output = []           
    operators = []        
    i = 0
    length = len(expression)

    while i < length:
        char = expression[i]

    
        if char.isspace():
            i += 1
            continue

        
        if char.isdigit() or char == '.':
            num = ''
            while i < length and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            output.append(num)
            continue

        if char.isalpha():
            func = ''
            while i < length and expression[i].isalpha():
                func += expression[i]
                i += 1
            if func in FUNCTIONS:
                operators.append(func)
            else:
                raise ValueError(f"تابع ناشناخته: {func}")
            continue

        if char == '(':
            operators.append(char)
            i += 1
            continue

        
        if char == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("پرانتز بسته بدون پرانتز باز معادل")
            operators.pop()  
            continue

        
        if char in PRECEDENCE:
            while (operators and operators[-1] != '(' and #تا وقتی که استک خالی نیست و بالای استک پرانتز نیست
                   (PRECEDENCE.get(operators[-1], 0) > PRECEDENCE[char] or
                    (PRECEDENCE.get(operators[-1], 0) == PRECEDENCE[char] and char != '^'))):
                output.append(operators.pop())
            operators.append(char)
            i += 1
            continue

        raise ValueError(f"کاراکتر نامعتبر: {char}")

    # خالی کردن بقیه عملگرها
    while operators:
        if operators[-1] == '(':
            raise ValueError("پرانتز باز بدون پرانتز بسته معادل")
        output.append(operators.pop())

    return output


def evaluate_postfix(postfix):
    
    
  
    stack = []

    for token in postfix:
        if is_number(token):
            stack.append(float(token))

        elif token in FUNCTIONS:
            if not stack:
                raise ValueError(f"عملوند کافی برای تابع {token} وجود ندارد")
            arg = stack.pop()

            
            if token in ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan']:
                if token in ['arcsin', 'arccos', 'arctan']:
                    
                    result = FUNCTIONS[token](arg) * 180 / math.pi
                else:
                   
                    result = FUNCTIONS[token](math.radians(arg))
            else:
                result = FUNCTIONS[token](arg)

            stack.append(result)

        else:  # عملگرهای دوتایی
            if len(stack) < 2:
                raise ValueError(f"عملوند کافی برای عملگر {token} وجود ندارد")
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("تقسیم بر صفر!")
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)
            else:
                raise ValueError(f"عملگر ناشناخته: {token}")

    if len(stack) != 1:
        raise ValueError("عبارت نادرست است (تعداد عملوندها مشکل دارد)")

    return stack[0]


def calculate(expression):
    
    try:
        postfix = infix_to_postfix(expression.replace(' ', ''))
        result = evaluate_postfix(postfix)
        return result
    except Exception as e:
        return f"خطا: {str(e)}"

