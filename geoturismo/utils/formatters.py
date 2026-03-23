def formatar_avaliacao(avaliacao, total):
    if avaliacao is None:
        return "Sem avaliação"
    if total is None:
        return f"{avaliacao}"
    return f"{avaliacao} ({total} avaliações)"