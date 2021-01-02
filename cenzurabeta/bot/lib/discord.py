import requests
import config

url = "https://discord.com/api/v8"
headers = {"authorization": f"Bot {config.token}"}

def get_guild_audit_log(guild):
    return requests.get(url + "/guilds/" + guild + "/audit-logs", headers=headers).json()

def get_channel(channel):
    return requests.get(url + "/channels/" + channel, headers=headers).json()

def modify_channel(channel, data):
    return requests.patch(url + "/channels/" + channel, headers=headers, json=data)

def delete_channel(channel):
    return requests.patch(url + "/channels/" + channel, headers=headers)

def get_messages(channel, limit=100):
    return requests.get(url + "/channels/" + channel + f"/messages?limit={limit}", headers=headers).json()

def get_message(channel, message):
    return requests.get(url + "/channels/" + channel + "/messages/" + message, headers=headers).json()

def create_message(channel, data, files=None):
    if files:
        return requests.post(url + "/channels/" + channel + "/messages", headers=headers, data=data, files=files)
    
    return requests.post(url + "/channels/" + channel + "/messages", headers=headers, json=data)

def crosspost_message(channel, message):
    return requests.post(url + "/channels/" + channel + "/messages/" + message + "/crosspost", headers=headers)

def create_reaction(channel, message, emoji):
    return requests.put(url + "/channels/" + channel + "/messages/" + message + "/reactions/" + emoji + "/@me", headers=headers)

def delete_reaction(channel, message, emoji):
    return requests.delete(url + "/channels/" + channel + "/messages/" + message + "/reactions/" + emoji + "/@me", headers=headers)

def delete_user_reaction(channel, message, emoji, user):
    return requests.delete(url + "/channels/" + channel + "/messages/" + message + "/reactions/" + emoji + "/" + user, headers=headers)

def get_reactions(channel, message, emoji):
    return requests.get(url + "/channels/" + channel + "/messages/" + message + "/reactions/" + emoji, headers=headers).json()

def delete_all_reactions(channel, message):
    return requests.delete(url + "/channels/" + channel + "/messages/" + message + "/reactions", headers=headers)

def delete_all_reactions_for_emoji(channel, message, emoji):
    return requests.delete(url + "/channels/" + channel + "/messages/" + message + "/reactions/" + emoji, headers=headers)

def edit_message(channel, message, data):
    return requests.patch(url + "/channels/" + channel + "/messages/" + message, headers=headers, json=data)

def delete_message(channel, message):
    return requests.delete(url + "/channels/" + channel + "/messages/" + message, headers=headers)

def bulk_delete_messages(channel, data):
    return requests.post(url + "/channels/" + channel + "/messages/bulk-delete", headers=headers, json=data)

def edit_channel_permissions(channel, overwrite, data):
    return requests.put(url + "/channels/" + channel + "/permissions/" + overwrite, headers=headers, json=data)

def get_channel_invites(channel):
    return requests.get(url + "/channels/" + channel + "/invites", headers=headers).json()

def create_channel_invite(channel, data):
    return requests.post(url + "/channels/" + channel + "/invites", headers=headers, json=data)

def delete_channel_permission(channel, overwrite):
    return requests.delete(url + "/channel/" + channel + "/permissions/" + overwrite, headers=headers)

def follow_news_channel(channel, data):
    return requests.post(url + "/channels/" + channel + "/followers", headers=headers, json=data)

def trigger_typing_indicator(channel):
    return requests.post(url + "/channels/" + channel + "/typing", headers=headers)

def get_pinned_messages(channel):
    return requests.get(url + "/channels/" + channel + "/pins", headers=headers).json()

def add_pinned_channel_message(channel, message):
    return requests.put(url + "/channels/" + channel + "/pins/" + message, headers=headers)

def delete_pinned_channel_message(channel, message):
    return requests.delete(url + "/channels/" + channel + "/pins/" + message, headers=headers)

def group_dm_add_recipient(channel, user):
    return requests.put(url + "/channels/" + channel + "/recipients/" + user, headers=headers)

def group_dm_remove_recipient(channel, user):
    return requests.delete(url + "/channels/" + channels + "/recipients/" + user, headers=headers)

def list_guild_emojis(guild):
    return requests.get(url + "/guilds/" + guild + "/emojis", headers=headers).json()

def get_guild_emoji(guild, emoji):
    return requests.get(url + "/guilds/" + guild + "/emojis" + emoji, headers=headers).json()

def create_guild_emoji(guild, data):
    return requests.post(url + "/guilds/" + guild + "/emojis", headers=headers)

def modify_guild_emoji(guild, emoji, data):
    return requests.patch(url + "/guilds/" + guild + "/emojis/" + emoji, headers=headers)

def delete_guild_emoji(guild, emoji):
    return requests.delete(url + "/guilds/" + guild + "/emojis/" + emoji, headers=headers)

def create_guild(data):
    return requests.post(url + "/guilds", headers=headers, json=data)

def get_guild(guild):
    return requests.get(url + "/guilds/" + guild, headers=headers).json()

def get_guild_preview(guild):
    return requests.get(url + "/guilds/" + guild + "/preview", headers=headers).json()

def modify_guild(guild, data):
    return requests.patch(url + "/guilds/" + guild, headers=headers, json=data)

def delete_guild(guild):
    return requests.delete(url + "/guilds/" + guild, headers=headers)

def get_guild_channels(guild):
    return requests.get(url + "/guilds/" + guild + "/channels", headers=headers).json()

def create_guild_channel(guild, data):
    return requests.post(url + "/guilds/" + guild + "/channels", headers=headers, json=data)

def modify_guild_channel_positions(guild, data):
    return requests.patch(url + "/guilds/" + guild + "/channels", headers=headers, json=data)

def get_guild_member(guild, user):
    return requests.get(url + "/guilds/" + guild + "/members/" + user, headers=headers).json()

def list_guild_members(guild, limit=1000, after=0):
    return requests.get(url + "/guilds/" + guild + f"/members?limit={limit}&after={after}", headers=headers).json()

def add_guild_member(guild, user):
    return requests.put(url + "/guilds/" + guild + "/members/" + user, headers=headers)

def modify_guild_member(guild, user, data):
    return requests.patch(url + "/guilds/" + guild + "/members/" + user, headers=headers, json=data)

def modify_current_user_nick(guild, data):
    return requests.patch(url + "/guilds/" + guild + "/members/@me/nick", headers=headers, json=data)

def add_guild_member_role(guild, user, role):
    return requests.put(url + "/guilds/" + guild + "/members/" + user + "/roles/" + role, headers=headers)

def remove_guild_member_role(guild, user, role):
    return requests.delete(url + "/guilds/" + guild + "/members/" + user + "/roles/" + role, headers=headers)

def remove_guild_member(guild, user):
    return requests.delete(url + "/guilds/" + guild + "/members/" + user, headers=headers)

def get_guild_bans(guild):
    return requests.get(url + "/guilds/" + guild + "/bans", headers=headers).json()

def get_guild_ban(guild, user):
    return requests.get(url + "/guilds/" + guild + "/bans/" + user, headers=headers).json()

def create_guild_ban(guild, user, reason=None, delete_message_days=0):
    return requests.put(url + "/guilds/" + guild + "/bans/" + user + f"?delete_message_days={delete_message_days}&reason={reason}", headers=headers)

def remove_guild_ban(guild, user):
    return requests.delete(url + "/guilds/" + guild + "/bans/" + user, headers=headers)

def get_guild_roles(guild):
    return requests.get(url + "/guilds/" + guild + "/roles", headers=headers).json()

def create_guild_role(guild, data):
    return requests.post(url + "/guilds/" + guild + "/roles", headers=headers, json=data)

def modify_guild_role_positions(guild, data):
    return requests.patch(url + "/guilds/" + guild + "/roles", headers=headers, json=data)

def modify_guild_role(guild, role, data):
    return requests.patch(url + "/guilds/" + guild + "/roles/" + role, headers=headers, json=data)

def delete_guild_role(guild, role):
    return requests.delete(url + "/guilds/" + guild + "/roles" + role, headers=headers)

def get_guild_prune_count(guild, days=7, include_roles=""):
    return requests.get(url + "/guilds/" + guild + f"/prune?days={days}&include_roles={include_roles}", headers=headers).json()

def begin_guild_prune(guild, data):
    return requests.post(url + "/guilds/" + guild + "/prune", headers=headers, json=data)

def get_guild_voice_regions(guild):
    return requests.get(url + "/guilds/" + guild + "/regions", headers=headers).json()

def get_guild_invites(guild):
    return requests.get(url + "/guilds/" + guild + "/invites", headers=headers).json()

def get_guild_integrations(guild):
    return requests.get(url + "/guilds/" + guild + "/integrations", headers=headers).json()

def create_guild_integration(guild, data):
    return requests.post(url + "/guilds/" + guild + "/integrations", headers=headers, json=data)

def modify_guild_integration(guild, integration, data):
    return requests.patch(url + "/guilds/" + guild + "/integrations/" + integration, headers=headers, json=data)

def delete_guild_integration(guild, integration):
    return requests.delete(url + "/guilds/" + guild + "/integrations/" + integration, headers=headers)

def sync_guild_integration(guild, integration):
    return requests.post(url + "/guilds/" + guild + "/integrations/" + integration + "/sync", headers=headers)

def get_guild_widget_settings(guild):
    return requests.get(url + "/guilds/" + guild + "/widget", headers=headers).json()

def modify_guild_widget(guild, data):
    return requests.patch(url + "/guilds/" + guild + "/widget", headers=headers, json=data)

def get_guild_widget(guild):
    return requests.get(url + "/guilds/" + guild + "/widget.json", headers=headers).json()

def get_guild_vanity_url(guild):
    return requests.get(url + "/guilds/" + guild + "/vanity-url", headers=headers).json()

def get_guild_widget_image(guild):
    return requests.get(url + "/guilds/" + guild + "/widget.png", headers=headers).json()

def get_invite(invite):
    return requests.get(url + "/invites/" + invite, headers=headers).json()

def delete_invite(invite):
    return requests.delete(url + "/invites/" + invite, headers=headers)

def get_template(template):
    return requests.get(url + "/guilds/templates/" + templatem, headers=headers).json()

def create_guild_from_template(template, data):
    return requests.post(url + "/guilds/templates/" + template, headers=headers, json=data)

def get_guild_templates(guild):
    return requests.get(url + "/guilds/" + guild + "/templates", headers=headers).json()

def create_guild_template(guild, data):
    return requests.post(url + "/guilds/" + guild + "/templates", headers=headers, json=data)

def sync_guild_template(guild, template):
    return requests.put(url + "/guilds/" + guild + "/templates/" + template, headers=headers)

def modify_guild_template(guild, template, data):
    return requests.patch(url + "/guilds/" + guild + "/templates/" + template, headers=headers, json=data)

def delete_guild_template(guild, template):
    return requests.delete(url + "/guilds/" + guild + "/templates/" + template)

def get_current_user():
    return requests.get(url + "/users/@me", headers=headers).json()

def get_user(user):
    return requests.get(url + "/users/" + user, headers=headers).json()

def modify_current_user(data):
    return requests.patch(url + "/users/@me", headers=headers, json=data)

def get_current_user_guilds():
    return requests.get(url + "/users/@me/guilds", headers=headers).json()

def leave_guild(guild):
    return requests.delete(url + "/users/@me/guilds/" + guild, headers=headers)

def get_user_dms():
    return requests.get(url + "/users/@me/channels", headers=headers).json()

def create_dm(data):
    return requests.post(url + "/users/@me/channels", headers=headers, json=data)

def create_group_dm(data):
    return requests.post(url + "/users/@me/channels", headers=headers, json=data)

def get_user_connections():
    return requests.get(url + "/users/@me/connections", headers=headers).json()

def list_voice_regions():
    return requests.get(url + "/voice/regions", headers=headers).json()

def create_webhook(channel, data):
    return requests.post(url + "/channels/" + channel + "/webhooks", headers=headers, json=data)

def get_channel_webhooks(channel):
    return requests.get(url + "/channels/" + channel + "/webhooks", headers=headers).json()

def get_guild_webhooks(guild):
    return requests.get(url + "/guilds/" + guild + "/webhooks", headers=headers).json()

def get_webhook(webhook):
    return requests.get(url + "/webhooks/" + webhook, headers=headers).json()

def get_webhook_with_token(webhook_id, webhook_token):
    return requests.get(url + "/webhooks/" + webhook_id + "/" + webhook_token, headers=headers).json()

def modify_webhook(webhook, data):
    return requests.patch(url + "/webhooks/" + webhook, headers=headers, json=data)

def modify_webhook_with_token(webhook_id, webhook_token, data):
    return requests.patch(url + "/webhooks/" + webhook_id + "/" + webhook_token, headers=headers, json=data)

def delete_webhook(webhook):
    return requests.delete(url + "/webhooks/" + webhook, headers=headers)

def delete_webhook_with_token(webhook_id, webhook_token):
    return requests.delete(url + "/webhooks/" + webhook_id + "/" + webhook_token, headers=headers)

def execute_webhook(webhook_id, webhook_token, data):
    return requests.post(url + "/webhooks/" + webhook_id + "/" + webhook_token, headers=headers, json=data)

def execute_slack_compatible_webhook(webhook_id, webhook_token, data):
    return requests.post(url + "/webhooks/" + webhook_id + "/" + webhook_token + "/slack", headers=headers, json=data)

def execute_github_compatible_webhook(webhook_id, webhook_token, data):
    return requests.post(url + "/webhooks/" + webhook_id + "/" + webhook_token + "/github", headers=headers, json=data)

def edit_webhook_message(webhook_id, webhook_token, message, data):
    return requests.patch(url + "/webhooks/" + webhook_id + "/" + webhook_token + "/messages/" + message, headers=headers, json=data)

def delete_webhook_message(webhook_id, webhook_token, message):
    return requests.delete(url + "/webhooks/" + webhook_id + "/" + webhook_token + "/messages/" + message, headers=headers, json=data)