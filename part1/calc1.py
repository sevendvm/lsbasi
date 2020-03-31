# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, DIVIDE, MULTIPLICATE, WHITESPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLICATE', 'WHITESPACE', 'EOF '


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, WHITESPACE or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', '-', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        # text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        # self.current_char = self.text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = Token(INTEGER, self.integer())
                # self.advance()
                return token

            if self.current_char == '+':
                token = Token(PLUS, self.current_char)
                self.advance()
                return token

            if self.current_char == '-':
                token = Token(MINUS, self.current_char)
                self.advance()
                return token
            
            if self.current_char == '/':
                token = Token(DIVIDE, self.current_char)
                self.advance()
                return token

            if self.current_char == '*':
                token = Token(MULTIPLICATE, self.current_char)
                self.advance()
                return token
            
        self.error()

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value
        
    def expr(self):
        """expr -> INTEGER PLUS INTEGER
        OR expr -> INTEGER MINUS INTEGER"""

        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            # we expect the current token to be a single-digit integer
            # left = self.current_token
            # self.eat(INTEGER)
    
            # we expect the current token to be a '+' token
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)
            elif op.type == DIVIDE:
                self.eat(DIVIDE)
            elif op.type == MULTIPLICATE:
                self.eat(MULTIPLICATE)
    
            # we expect the current token to be a single-digit integer
            right = self.term()
            
            # after the above call the self.current_token is set to
            # EOF token
    
            # at this point INTEGER PLUS INTEGER sequence of tokens
            # has been successfully found and the method can just
            # return the result of adding two integers, thus
            # effectively interpreting client input
            if op.type == PLUS:
                result = result + right
            elif op.type == MINUS:
                result = result - right
            elif op.type == DIVIDE:
                if right.value == 0:
                    self.error()
                else:
                    result = result / right
            elif op.type == MULTIPLICATE:
                result = result * right
            else:
                result = None
                self.error()
            
            # left.value = result
            
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
