# Validador de CPF
cpf = input('Digite o seu CPF: ')
# Formata e adiciona os numeros do CPF numa lista
cpfFormatado = []
for i in cpf:
    if i != '.' and i != '-':
        cpfFormatado.append(int(i))
cpfVerificar = cpfFormatado[:9]
# Verifica e inclue o primeiro digito após o hifen
reverso = 10
somaDigitos = 0
for digito in cpfVerificar:
    somaDigitos += digito * reverso
    reverso -= 1
    if reverso == 1:
        break
if (11 - somaDigitos % 11) > 9:
    penultimoDigito = 0
else:
    penultimoDigito = (11 - somaDigitos % 11)
cpfVerificar.append(penultimoDigito)
# Verifica e inclue o segundo digito após o hifen
reverso = 11
somaDigitos = 0
for digito in cpfVerificar:
    somaDigitos += digito * reverso
    reverso -= 1
    if reverso == 1:
        break
if (11 - somaDigitos % 11) > 9:
    ultimoDigito = 0
else:
    ultimoDigito = (11 - somaDigitos % 11)
cpfVerificar.append(ultimoDigito)
print(f"O CPF {cpf} é válido" if cpfVerificar == cpfFormatado else f"O CPF {cpf} é inválido.")