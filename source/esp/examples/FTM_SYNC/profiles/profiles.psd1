# FTM_SYNC - mapa de nodos fisicos -> perfiles de firmware.
# 5 placas, 2 imagenes distintas. Los nombres de nodo son etiquetas fisicas.
@{
    Profiles = @{
        ref      = @{ Defaults = 'fts_ref.defaults';      Role = 'master'; Target = 'esp32s3' }
        follower = @{ Defaults = 'fts_follower.defaults'; Role = 'slave';  Target = 'esp32s3' }
    }
    Nodes = @{
        REF = @{ Profile = 'ref';      Label = 'REF (referencia)' }
        F1  = @{ Profile = 'follower'; Label = 'F1 (seguidor 1)' }
        F2  = @{ Profile = 'follower'; Label = 'F2 (seguidor 2)' }
        F3  = @{ Profile = 'follower'; Label = 'F3 (seguidor 3)' }
        F4  = @{ Profile = 'follower'; Label = 'F4 (seguidor 4)' }
    }
    # Orden de defaults: comun; rol; consola; generado (GPIO/LED/WiFi desde config).
    DefaultsOrder = @('fts_common.defaults', '<role>', '<console>', '<generated>')
}
