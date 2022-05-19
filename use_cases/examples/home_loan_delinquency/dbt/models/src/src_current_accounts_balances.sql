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


-- Source data containing current accounts balances
--
-- This query selects data from the src_current_accounts_attributes source,
-- which contains current account balances which have been artificially manufactured.
-- To inspect the definition of the fields, generate the DBT documentation

SELECT
    ACCOUNT_KEY,
    CURRENT_BALANCE
FROM
    {{ source('sample_data', 'src_current_accounts_balances')}}
