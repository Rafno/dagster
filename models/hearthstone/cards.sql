{{
  config(
	materialized = 'table', schema = 'hearthstone'
	)
}}

with final as (
SELECT
	id AS card_id,
	collectible,
	slug,
	classId AS class_id,
	spellSchoolId AS spell_school_id,
	cardTypeId AS card_type_id,
	cardSetId AS card_set_id,
	rarityId AS rarity_id,
	artistName AS artist_name,
	manaCost AS mana_cost,
	name_en_US AS card_name,
	text_en_US AS card_text,
	image_en_US AS card_image,
	cropImage AS crop_image,
	keywordIds_0 AS keywords_0,
	keywordIds_1 AS keywords_1,
	keywordIds_2 AS keywords_2,
	isZilliaxFunctionalModule AS is_zilliax_functional_module,
	isZilliaxCosmeticModule AS is_zilliax_cosmetic_module,
	duels_relevant AS duels_relevant,
	duels_constructed AS duels_constructed,
	copyOfCardId AS copy_of_card_id,
	health,
	attack,
	minionTypeId AS minion_type_id
FROM
	{{ ref('stg_cards') }}

)

select * from final