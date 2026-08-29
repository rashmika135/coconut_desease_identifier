class_names = [
    'Healthy',
    'CCI',
    'WCLWD_Yellowing',
    'WCLWD_Flaccidity',
    'WCLWD_Drying'
]

label_map = {
    name: index
    for index, name in enumerate(class_names)
}
