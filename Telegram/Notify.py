from loguru import logger

def Parse(Token):

    Token['Notify'] = {}
    logger.debug(f'Generating notifications for {Token["Address"]}')

    Token['Notify']['Similar'] = bool(Token['Owner'].get('Similarity'))
    Token['Notify']['Duplicate'] = bool(Token.get('Duplicate'))
    Token['Notify']['Freezable'] = bool(Token['Data']['Solana']['Mint']['freeze_authority_option'])
    Token['Notify']['Mintable'] = bool(Token['Data']['Solana']['Mint']['mint_authority_option'])
    Token['Notify']['Mutable'] = bool(Token['Data']['Solana']['Metaplex']['is_mutable'])
    Token['Notify']['ZeroBalance'] = bool(Token['Data']['Solana']['Account'].get('Balance', 0) == 0)
    Token['Notify']['NoSocials'] = bool(not(Token['Data'].get('Website') or Token['Data'].get('Telegram') or Token['Data'].get('Twitter') or Token['Data'].get('Discord')))

    Token['Notify']['Safe'] = bool(not(Token['Notify']['Duplicate'] or Token['Notify']['Freezable'] or Token['Notify']['Mintable'] or Token['Notify']['Mutable'] or Token['Notify']['ZeroBalance']) and Token['Data'].get('Website') and Token['Data'].get('Telegram') and Token['Data'].get('Twitter'))

