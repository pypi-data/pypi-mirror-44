class RemoveMethod(object):
    DONT_REMOVE, FROM_SC, FROM_CONN, FROM_BOTH = range(4)


RemoveMethods = (
    (RemoveMethod.DONT_REMOVE, 'Dont remove'),
    (RemoveMethod.FROM_SC, 'Remove from Singular Center'),
    (RemoveMethod.FROM_CONN, 'Remove from Connector'),
    (RemoveMethod.FROM_BOTH, 'Remove from Singular Center and Connector'),
)


class ActivityType(object):
    TASK, EVENT, FIXED_TIME = range(3)


ActivityTypes = (
    (ActivityType.TASK, 'Task'),
    (ActivityType.EVENT, 'Event'),
    (ActivityType.FIXED_TIME, 'Fixed Time'),
)


class ActivityStatus(object):
    IN_BACKLOG, READY, SCHEDULED, DONE, CHECK = range(5)


ActivityStatuses = (
    ActivityStatus.IN_BACKLOG, 'In Backlog',
    ActivityStatus.READY, 'Ready',
    ActivityStatus.SCHEDULED, 'Scheduled',
    ActivityStatus.DONE, 'Done',
    ActivityStatus.CHECK, 'Check',
)


class UserStatus:
    ASKED, CONFIRMED, REJECTED = range(3)


UserStatuses = (
    (UserStatus.ASKED, 'ASKED'),
    (UserStatus.CONFIRMED, 'CONFIRMED'),
    (UserStatus.REJECTED, 'REJECTED'),
)


class RepeatMode:
    SINGLE, EVERY, AFTER = range(3)


RepeatModes = (
    (RepeatMode.SINGLE, 'SINGLE'),
    (RepeatMode.EVERY, 'EVERY'),
    (RepeatMode.AFTER, 'AFTER'),
)


class UserRole:
    SUPERVISOR = 'SUPERVISOR'
    EXECUTOR = 'EXECUTOR'


UserRoles = (
    (UserRole.SUPERVISOR, 'SUPERVISOR'),
    (UserRole.EXECUTOR, 'EXECUTOR')
)


class Color:
    red = '-red'
    pink = '-pink'
    purple = '-purple'
    deep_purple = '-deep-purple'
    indigo = '-indigo'
    blue = '-blue'
    light_blue = '-light-blue'  # default
    cyan = '-cyan'
    teal = '-teal'
    green = '-green'
    light_green = '-light-green'
    lime = '-lime'
    yellow = '-yellow'
    amber = '-amber'
    orange = '-orange'
    deep_orange = '-deep-orange'
    brown = '-brown'
    grey = '-grey'


colors_map = {
    Color.red: '#d32f2f',
    Color.pink: '#c2185b',
    Color.purple: '#7b1fa2',
    Color.deep_purple: '#512da8',
    Color.indigo: '#303f9f',
    Color.blue: '#1976d2',
    Color.light_blue: '#0288d1',
    Color.cyan: '#0097a7',
    Color.teal: '#00796b',
    Color.green: '#388e3c',
    Color.light_green: '#689f38',
    Color.lime: '#afb42b',
    Color.yellow: '#fbc02d',
    Color.amber: '#ffa000',
    Color.orange: '#f57c00',
    Color.deep_orange: '#e64a19',
    Color.brown: '#5d4037',
    Color.grey: '#616161',
}

color_default = Color.light_blue

Colors = (
    (Color.red, 'Red'),
    (Color.pink, 'Pink'),
    (Color.purple, 'Purple'),
    (Color.deep_purple, 'Deep Purple'),
    (Color.indigo, 'Indigo'),
    (Color.blue, 'Blue'),
    (Color.light_blue, 'Light Blue'),
    (Color.cyan, 'Cyan'),
    (Color.teal, 'Teal'),
    (Color.green, 'Green'),
    (Color.light_green, 'Light Green'),
    (Color.lime, 'Lime'),
    (Color.yellow, 'Yellow'),
    (Color.amber, 'Amber'),
    (Color.orange, 'Orange'),
    (Color.deep_orange, 'Deep Orange'),
    (Color.brown, 'Brown'),
    (Color.grey, 'Grey'),
)
