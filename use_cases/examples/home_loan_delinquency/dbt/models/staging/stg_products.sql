-- Copyright 2022 Google LLC

-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at

--     https://www.apache.org/licenses/LICENSE-2.0

-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.


-- Product reference data
--
-- This model selects active product reference data.
-- To inspect the definition of the fields, generate the DBT documentation

SELECT DISTINCT
    PRODUCT_ID      as product_id,
    PRODUCT_CODE    as product_code,
    PRODUCT_SUBCODE as product_subcode,
    DESCRIPTION     as description,
    ACTIVE_FLAG     as active_flag
FROM
    {{ ref('ref_products')}}
WHERE
    Active_Flag is true
