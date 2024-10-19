export const properDate = (day: string) => {
  const datePattern = /^\d{4}\d{2}\d{2}$/;
  return datePattern.test(day) && Number(day.slice(0, 4)) > 2019;
};
