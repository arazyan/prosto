def old_to_new(website: str) -> str:
  """"Эта функция переводит старый вебсайт на новую ссылку."""
  new_website = website.strip().split('/')[1:]
  res = '/'.join(['https://api.prostospb.team', *new_website])
  return res


# old_to_new('xn--90azaccdibh.xn--p1ai/api/form_participation.php?user_id=128770&event_id=9706 ')

