const areObjectsEqual = (
  obj1: Record<string, any>,
  obj2: Record<string, any>,
): boolean => {
  const keys1 = Object.keys(obj1)
  const keys2 = Object.keys(obj2)

  if (keys1.length !== keys2.length) return false

  for (const key of keys1) {
    if (obj1[key] !== obj2[key]) return false
  }

  return true
}
const checkFileType = (file: any, allowedFileTypes: any) => {
  // Checks if the file is of any in the given types
  if (!allowedFileTypes.includes(file.type)) {
    return false
  }
  return true
}

const checkMaxSize = (file: any, maxSizeInBytes: number) => {
  // Checks if the file size is below the given size
  if (file.size > maxSizeInBytes) {
    return false
  }
  return true
}

const clampNumber = (
  val: any,
  min: number = -Infinity,
  max: number = Infinity,
  decimalScale: number = 0,
): number => {
  let v = typeof val === 'number' ? val : Number(val)
  v = Math.min(max, Math.max(min, isNaN(v) ? 0 : v))
  return Number(v.toFixed(decimalScale))
}

const getWeekDays = () => [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
]

function formatFileSize(size: number) {
  var i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024))
  var n = parseFloat((size / Math.pow(1024, i)).toFixed(2))
  return n * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i]
}

const generateNumberRegex = (
  min: number,
  max: number,
  allowDecimal: boolean,
): RegExp => {
  const floatRegexStr = '(\\.[0-9]*)?'
  const negativeIntRegexStr = '-[0-9]*'
  const positiveIntRegexStr = '[0-9]+'
  const positiveOrNegativeIntRegexStr = '-?[0-9]*'

  let regexStr = '^'
  if (max < 0) regexStr += negativeIntRegexStr
  else if (min >= 0) regexStr += positiveIntRegexStr
  else regexStr += positiveOrNegativeIntRegexStr
  if (allowDecimal) regexStr += floatRegexStr
  regexStr += '$'
  return new RegExp(regexStr)
}

const getFormControlProps = (props: any) => ({
  color: props.color,
  disabled: props.disabled,
  error: props.error,
  fullWidth: props.fullWidth,
  required: props.required,
  variant: props.variant,
  sx: props.sx,
  size: props.size,
})

const getParentPath = (path: string, levelsUp: number = 1): string => {
  const pathArray = path.replace(/\/+$/, '').split('/')
  for (let i = 0; i < levelsUp; i++) pathArray.pop()
  return pathArray.join('/')
}

const getRecurrenceText = ({
  interval,
  type,
  daysOfWeek,
}: {
  interval: number
  type: 'daily' | 'weekly'
  daysOfWeek?: number[]
}) => {
  if (type === 'daily') {
    if (interval == 1) return 'Every day'
    if (interval == 2) return 'Alternate days'
    return `Every ${interval} days`
  } else if (type === 'weekly') {
    if (interval === 1) return `Every ${groupWeekdays(daysOfWeek!!)}`
    return `Every ${interval} week${interval > 1 ? 's' : ''} on ${groupWeekdays(
      daysOfWeek!!,
    )}`
  }
}

const weekDayToString = (dayNumber: number) => getWeekDays()[dayNumber]

function groupWeekdays(weekdayNumbers: number[]): string {
  const weekdays = getWeekDays()
  const groupedDays: string[] = []

  // Check if all days are present
  if (weekdayNumbers.length === 7) {
    return 'every day'
  }

  // Sort the input array for consecutive day grouping
  weekdayNumbers.sort((a, b) => a - b)

  let startDay: number | null = null
  let prevDay: number | null = null

  for (const day of weekdayNumbers) {
    if (startDay === null) {
      startDay = day
    } else if (prevDay !== null && day !== prevDay + 1) {
      // If there is a gap, add the range to the result
      if (startDay === prevDay) {
        groupedDays.push(weekdays[startDay])
      } else {
        groupedDays.push(`${weekdays[startDay]}–${weekdays[prevDay]}`)
      }
      startDay = day
    }
    prevDay = day
  }

  // Add the last range to the result
  if (startDay !== null) {
    if (startDay === prevDay || prevDay === null) {
      groupedDays.push(weekdays[startDay])
    } else {
      groupedDays.push(`${weekdays[startDay]}–${weekdays[prevDay]}`)
    }
  }

  return groupedDays.join(', ')
}

function stringToColor(string: string) {
  let hash = 0
  let i

  /* eslint-disable no-bitwise */
  for (i = 0; i < string.length; i += 1) {
    hash = string.charCodeAt(i) + ((hash << 5) - hash)
  }

  let color = '#'

  for (i = 0; i < 3; i += 1) {
    const value = (hash >> (i * 8)) & 0xff
    color += `00${value.toString(16)}`.slice(-2)
  }
  /* eslint-enable no-bitwise */

  return color
}

export {
  areObjectsEqual,
  checkFileType,
  checkMaxSize,
  clampNumber,
  formatFileSize,
  getWeekDays,
  generateNumberRegex,
  getFormControlProps,
  getParentPath,
  getRecurrenceText,
  weekDayToString,
  stringToColor,
}
