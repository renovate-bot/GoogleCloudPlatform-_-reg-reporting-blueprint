-- Copyright 2022 The Reg Reporting Blueprint Authors

-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at

--     https://www.apache.org/licenses/LICENSE-2.0

-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.


-- Reference data containing banking products information
--
-- This query selects the relevant fields from the ref_products source,
-- which contains reference data about banking products. To inspect the
-- definition of the fields, generate the DBT documentation

SELECT
    product_id,
    product_code,
    product_subcode,
    description,
    active_flag
FROM
    {{ source('sample_data', 'ref_products') }}
