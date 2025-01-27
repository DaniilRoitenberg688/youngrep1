function onClick(name) {
    fetch(
        '/add_statistic/'+name,
        {
            method: 'post'
        }
    )
}