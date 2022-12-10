[{
    $addFields: {
        socialArray: {
            $split: [
                '$Ke sledování novinek ze světa politiky a sociálních témat nejčastěji používám tato sociální média: ',
                ','
            ]
        },
        occupationArray: {
            $split: [
                '$V současné době',
                ','
            ]
        }
    }
}, {
    $addFields: {
        social0: {
            $arrayElemAt: [
                '$socialArray',
                0
            ]
        },
        social1: {
            $arrayElemAt: [
                '$socialArray',
                1
            ]
        },
        social2: {
            $arrayElemAt: [
                '$socialArray',
                2
            ]
        },
        social3: {
            $arrayElemAt: [
                '$socialArray',
                3
            ]
        },
        social4: {
            $arrayElemAt: [
                '$socialArray',
                4
            ]
        },
        occupation0: {
            $arrayElemAt: [
                '$occupationArray',
                0
            ]
        },
        occupation1: {
            $arrayElemAt: [
                '$occupationArray',
                1
            ]
        },
        occupation2: {
            $arrayElemAt: [
                '$occupationArray',
                2
            ]
        },
        occupation3: {
            $arrayElemAt: [
                '$occupationArray',
                3
            ]
        },
        occupation4: {
            $arrayElemAt: [
                '$occupationArray',
                4
            ]
        }
    }
}, {
    $project: {
        'Věk': 1,
        'Pohlaví': 1,
        social0: 1,
        social1: 1,
        social2: {
            $ifNull: [
                '$social2',
                null
            ]
        },
        social3: {
            $ifNull: [
                '$social3',
                null
            ]
        },
        social4: {
            $ifNull: [
                '$social4',
                null
            ]
        },
        occupation0: 1,
        occupation1: 1,
        occupation2: {
            $ifNull: [
                '$occupation2',
                null
            ]
        },
        occupation3: {
            $ifNull: [
                '$occupation3',
                null
            ]
        },
        occupation4: {
            $ifNull: [
                '$occupation4',
                null
            ]
        }
    }
}]