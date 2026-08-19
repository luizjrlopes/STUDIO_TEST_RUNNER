# Studio Test Runner

[English](README.md) | [Português](README.pt-BR.md)

Runner externo de conformidade e regressão para distribuições do **Studio V5**. Ele não reimplementa o runtime do Studio. Em vez disso, inspeciona uma árvore materializada do Studio, executa cenários declarativos, avalia invariantes, compara snapshots e produz relatórios ricos em evidências.

## Por que este repositório existe

O Studio V5 já possui routing, estado, agentes, writers, handoffs e gates. Este projeto é deliberadamente independente: sua função é provar que uma distribuição continua obedecendo a essas regras depois de mudanças.

O runner responde a perguntas como:

- os arquivos e boundaries obrigatórios estão presentes?
- um Specialist consegue escrever apenas em seu próprio `specialist_report` dentro de `.studio`?
- Area Owners permanecem dentro da própria área?
- o Super Owner coordena boundaries sem alterar o estado local de outra área?
- referências de handoff e targets declarados podem ser resolvidos?
- snapshots esperados continuam correspondendo ao comportamento observado?

## Início rápido

As suítes embutidas não exigem dependências de runtime de terceiros.

```bash
python -m studio_test_runner --help
python -m studio_test_runner run fixtures/valid --suite suites/orchestration-core.json
python -m studio_test_runner run fixtures/invalid_specialist_write --suite suites/specialist-scope.json
python -m studio_test_runner regress snapshots/baseline.json snapshots/candidate.json
```

A partir de um checkout do código, instale em modo editável ou defina `PYTHONPATH=src`:

```bash
PYTHONPATH=src python -m studio_test_runner run fixtures/valid --suite suites/orchestration-core.json --report-dir reports
```

## Saídas

Cada execução pode produzir:

- resumo no terminal;
- `report.json` para automação;
- `report.md` para revisão;
- `report.html` para portfólio/demonstração.

Códigos de saída:

- `0`: todas as assertions passaram;
- `1`: pelo menos uma assertion falhou;
- `2`: comando ou input inválido.

## Formato dos cenários

As suítes são JSON e permanecem intencionalmente declarativas.

```json
{
  "id": "orchestration-core",
  "assertions": [
    {"type": "path_exists", "path": ".studio/GENERAL_ORCHESTRATION"},
    {"type": "specialist_write_scope"},
    {"type": "owner_cross_area_write"}
  ]
}
```

## Princípios de design

- **verificador externo** — nunca se torna um segundo runtime do Studio;
- **deny by default** — assertions de escopo falham de forma fechada;
- **evidence first** — toda assertion retorna paths e detalhes observados;
- **núcleo determinístico** — nenhum LLM é necessário para verificações de conformidade;
- **portável** — apenas a biblioteca padrão do Python é necessária para o núcleo;
- **superfície pequena** — assertions são componíveis e auditáveis.

Veja [`docs/architecture.md`](docs/architecture.md), [`docs/assertions.md`](docs/assertions.md) e [`docs/scenario-authoring.md`](docs/scenario-authoring.md).
