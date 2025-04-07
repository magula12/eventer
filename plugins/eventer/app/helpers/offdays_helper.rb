module OffdaysHelper

  def formatted_offday_time(time)
    "#{time.strftime('%A %d. %B %Y %H:%M')}"
  end
  def cleanup_expired_off_days_for(user_id)
    OffDay.where("user_id = ? AND end_datetime < ?", user_id, Time.current).destroy_all
  end

end
