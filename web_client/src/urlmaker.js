export default function urlmaker (productsCount, productsByPage, pageNumber,
                activePage, orderBy, priceFrom, priceTo,
                queryText, categorySlug, matchPhrase, shopSlug, activeCategory, parent) {

      const from = productsCount > productsByPage * pageNumber ? (
            productsByPage * pageNumber
        ) : (
            activePage * productsByPage
        );

      const sort = () => {
        if (orderBy === '-created_at') {
            return {created_at: 'desc'}
        } else if (orderBy === 'title'){
            return {title: 'asc'}
        } else if (orderBy === 'price') {
            return {get_price_function: 'asc'}
        } else if (orderBy === '-price') {
            return {get_price_function: 'desc'}
        }
      };

      const sorting = () => {
            if (priceFrom && priceTo) {
                return [{range: {get_price_function: {gte: priceFrom}}},
                    {range: {get_price_function: {lte: priceTo}}}]
            } else if (priceFrom) {
                return [
                    {range: {get_price_function: {gte: priceFrom}}}
                ]
            } else if (priceTo) {
                return [
                    {range: {get_price_function: {lte: priceTo}}}
                ]
            }
      };


      const q = () => {
        if (queryText && activeCategory !== '') {
            return [
                { match: { text:  queryText }},
                { match_phrase: matchPhrase },
                { match_phrase: { category_id: activeCategory }}
            ]
        } else if (queryText) {
            return [
                { match: { text:  queryText }},
                { match_phrase: matchPhrase },
            ]
        } else if (activeCategory && parent) {
            return [
                { match_phrase: { parent_category_id: activeCategory }},
                { match_phrase: matchPhrase},
            ]
        } else if (activeCategory && !parent) {
            return [
                { match_phrase: { category_id: activeCategory }},
                { match_phrase: matchPhrase},
            ]
        } else {
            return [
                { match_phrase: matchPhrase}
            ]
        }
      };

        const query = {
            query: {
                    bool: {
                        must: q(),
                        filter: sorting()
                    }

                  },
            size:  productsByPage,
            from: pageNumber === 1 ? 0 : from,
            sort: [
                sort(),
            ],
          };

      return query

}
