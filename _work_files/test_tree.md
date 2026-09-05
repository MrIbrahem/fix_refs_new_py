```
tests/
├── bots/
│   ├── add_lang_en_bot/
│   │   └── test_bots_add_lang_en.py
│   ├── expend_refs/
│   │   └── test_bots_expend_refs.py
│   ├── fix_images/
│   │   └── test_fix_images.py
│   ├── fix_missing_refs/
│   │   └── test_missing_refs.py
│   ├── mini_fixes/
│   │   ├── test_bots_mini_fixes.py
│   │   └── test_mini_fixes.py
│   ├── months/
│   │   └── test_months.py
│   ├── move_dots/
│   │   └── test_move_dots.py
│   ├── remove_duplicate_refs/
│   │   ├── texts/
│   │   │   ├── expected.txt
│   │   │   ├── input.txt
│   │   │   └── output.txt
│   │   └── test_bots_remove_duplicate_refs.py
│   └── texts/
│       ├── expend_input.txt
│       └── expend_output.txt
├── core/
│   ├── texts/
│   │   ├── ja/
│   │   │   ├── expected.txt
│   │   │   ├── input.txt
│   │   │   └── output.txt
│   │   └── pl/
│   │       ├── expected.txt
│   │       ├── input.txt
│   │       └── output.txt
│   ├── test_fix_page.py
│   ├── test_fix_page_files.py
│   ├── test_fix_refs.py
│   └── test_index.py
├── infobox/
│   ├── texts_infobox2/
│   │   ├── expected.txt
│   │   ├── input.txt
│   │   └── output.txt
│   ├── test_do_comments.py
│   ├── test_infobox2.py
│   ├── test_infobox_expend_infobox.py
│   └── test_infobox_expend_infobox_2.py
├── lang_bots/
│   ├── bg_bot/
│   │   ├── test_bulgarian_bot.py
│   │   └── test_lang_bots_bg.py
│   ├── es/
│   │   ├── mv_es_refs_texts/
│   │   │   ├── 1/
│   │   │   │   ├── expected.txt
│   │   │   │   ├── input.txt
│   │   │   │   └── output.txt
│   │   │   └── 2/
│   │   │       ├── expected.txt
│   │   │       ├── input.txt
│   │   │       └── output.txt
│   │   ├── test_lang_bots_es.py
│   │   ├── test_lang_bots_es_additional.py
│   │   ├── test_lang_bots_es_section.py
│   │   └── test_mv_es_refs.py
│   ├── hy_bots/
│   │   ├── test_armenian_bot.py
│   │   ├── test_lang_bots_hy.py
│   │   └── test_remove_spaces_between_ref_and_punctuation.py
│   ├── pl_bots/
│   │   ├── test_pl_bot.py
│   │   └── test_polish_bot.py
│   ├── pt_bots/
│   │   ├── test_lang_bots_pt.py
│   │   └── test_pt_months_new_value.py
│   ├── remove_space/
│   │   ├── remove_space_texts/
│   │   │   ├── 1/
│   │   │   │   ├── expected.txt
│   │   │   │   ├── input.txt
│   │   │   │   └── output.txt
│   │   │   └── 2/
│   │   │       ├── expected.txt
│   │   │       ├── input.txt
│   │   │       └── output.txt
│   │   ├── run_files.py
│   │   ├── test_files.py
│   │   ├── test_remove_space.py
│   │   └── test_remove_space_part_2.py
│   └── sw_bot/
│       ├── test_lang_bots_sw.py
│       └── test_swahili_bot.py
├── mdwiki/
│   ├── test_category_network.py
│   └── test_mdwiki_category.py
├── parsers/
│   ├── test_category.py
│   ├── test_citations_parser.py
│   └── test_parsers_category.py
├── utils/
├── __init__.py
├── conftest.py
└── README.md

```