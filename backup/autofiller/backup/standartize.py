def old_to_new(website: str) -> str:
  """"Эта функция переводит старый вебсайт на новую ссылку."""
  new_website = [x for x in website.strip().split('/')[1:] if 'xn' not in x and x != '']
  res = '/'.join(['https://api.prostospb.team', *new_website])
  return res


