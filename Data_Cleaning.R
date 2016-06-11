# Script that cleans data from Airbnb Kaggle challenge for clustering

#Read in data 
traindata <- read.csv("~/Airbn/train_users_2.csv", header = TRUE)
summary(traindata)

#Remove useless columns ----
traindata$timestamp_first_active <- NULL
traindata$date_first_booking <- NULL
traindata$language <- NULL #too sparse 
traindata$signup_app <- NULL 

traindata$age <- NULL

#Fine-tuning with other columns of the data----

# Isolate the month from account creation 

dac <- data.frame(matrix(nrow = length(traindata$date_account_created)))
for(i in 1:length(traindata$date_account_created)){
  delete <- as.numeric(strsplit(as.character(traindata$date_account_created[i]), "/")[[1]][1])
  dac[i,1] <- delete
}
dac <- as.factor(as.numeric(dac[,1]))

traindata$date_account_created <- dac

# Change "Other" gender to FEMALE (mode)
traindata$gender[traindata$gender== "OTHER"] = "FEMALE"
traindata$gender <- droplevels(traindata$gender)

# Signup_flow refers to origin page 
hist(traindata$signup_flow)
table(traindata$signup_flow)

# Assign outlier pages to mode, 2. 
traindata$signup_flow[traindata$signup_flow == 1] = 0
traindata$signup_flow[traindata$signup_flow == 6] = 3
traindata$signup_flow[traindata$signup_flow == 8] = 3
traindata$signup_flow[traindata$signup_flow == 24] = 3

traindata$signup_flow <- as.factor(traindata$signup_flow)
# Change missing values in first_affliate_tracked to `untracked` 
# Change `product` to `tracked-other` 
traindata$first_affiliate_tracked <- as.character(traindata$first_affiliate_tracked)
traindata$first_affiliate_tracked[is.na(traindata$first_affiliate_tracked)] = "untracked"
traindata$first_affiliate_tracked[traindata$first_affiliate_tracked == "product"] = "tracked-other"
traindata$first_affiliate_tracked <- as.factor(traindata$first_affiliate_tracked)

# Combine smaller levels in `first_device_type` to other 
levels(traindata$first_device_type)
levels(traindata$first_device_type) <- c("Other/Unknown", "Other/Unknown", "Other/Unknown",
                                         "Other/Unknown", "Other/Unknown", "Mac Desktop",
                                         "Other/Unknown", "Windows Desktop")

# Combine smaller levelws in `first_browser` 
table(traindata$first_browser)

levels(traindata$first_browser) <- c("Other", "Other","Other", "Chrome", 
                                     "Other","Other","Firefox", "Other",
                                     "Other","Other","Other","Other",
                                     "Other","Safari", "Other")

# Combine smaller levels in `country_destition` 

levels(traindata$country_destition) <- c("Other","CA", "Other","ES", "FR", 
                                         "Other","Other","NDF", "Other","Other","Other","US")
#Combine smaller levels in 'affiliate_channel` 

levels(traindata$affiliate_channel) <- c("other", "direct", "other", "sem", "sem", "other")

# Combine levels of affiliate_provider 

levels(traindata$affiliate_provider) <- c("craigslist", "direct", "other", "google", "other", "other")

# Change levels of `date_account_created` to seasons 
levels(traindata$date_account_created) <- c("winter", "winter","spring","spring", "spring","spring",
                                            "summer", "summer","summer","fall","fall","winter")

# Produce dummy variables ----
library(dummies)
finaldf <- data.frame(traindata$id)

col1 <- data.frame(dummy(traindata$date_account_created))
col2 <- data.frame(dummy(traindata$gender))
col3 <- data.frame(dummy(traindata$signup_method))
col4 <- data.frame(dummy(traindata$affiliate_channel))
col5 <- data.frame(dummy(traindata$affiliate_provider))
col6 <- data.frame(dummy(traindata$first_affiliate_tracked))
col7 <- data.frame(dummy(traindata$first_device_type))
col8 <- data.frame(dummy(traindata$first_browser))
col9 <- data.frame(dummy(traindata$country_destition))

#Combine into one data frame 
finaldf <- cbind(finaldf, col1, col2, col3, col4, col5, col6, col7, col8, col9)

#Write to csv 
write.csv(finaldf, file = "~/Airbnb_cluster.csv", row.names = FALSE)
