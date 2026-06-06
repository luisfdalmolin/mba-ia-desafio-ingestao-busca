from search import search_prompt
from database import similarity_search

def main():
    chain = search_prompt()

    try:
        while True:
            question = input('\nQUAL A SUA PERGUNTA?: ').strip()

            if not question:
                continue

            result = chain.invoke({'contexto': similarity_search(question), 'pergunta': question})

            print(f'\nAQUI ESTÁ SUA RESPOSTA:\n')
            print(result.content.strip())

    except KeyboardInterrupt:
        print('\n\nChat finalizado pelo usuário\n')

if __name__ == '__main__':
    main()
