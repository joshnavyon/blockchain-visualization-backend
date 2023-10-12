MATCH (wallet:wallet {addressId: '0x8d08aad4b2bac2bb761ac4781cf62468c9ec47b4'})
OPTIONAL MATCH (wallet)-[s:RECEIVED_FROM]->(wallet_in)
OPTIONAL MATCH (wallet)-[r:SENT_TO]->(wallet_out)
WITH wallet, wallet_in, wallet_out, s, r
ORDER BY s.block_timestamp DESC
WITH wallet, wallet_in, wallet_out, COLLECT(DISTINCT s)[0] AS latest_sender, COLLECT(DISTINCT r)[0] AS latest_recipient
WITH wallet,
COLLECT(DISTINCT wallet_in) AS wallet_in_list,
COLLECT(DISTINCT wallet_out) AS wallet_out_list,
COLLECT(DISTINCT latest_sender) AS latest_in,
COLLECT(DISTINCT latest_recipient) AS latest_out
RETURN wallet,
wallet_in_list AS walletIn,
wallet_out_list AS walletOut,
latest_in AS latestIn,
latest_out AS latestOut;