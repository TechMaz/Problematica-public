routers = dict(
    BASE=dict(
        default_application='Problematica',
        default_controller='default',
        default_function='index',
    ),
)

routes_in = (
  ('/$f', '/problematica/default/$f'),
)

routes_onerror = [
  ('*/404', '/pagenotfound.html')
]

routes_out = [(x, y) for (y, x) in routes_in]
